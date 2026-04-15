import threading
import pandas as pd
import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.exceptions import BadRequest
from jobspy import scrape_jobs
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# --- Configuration ---
CSV_FILE = 'jobs_cache.csv'
ALLOWED_COUNTRIES = ['USA', 'India', 'UK', 'Canada', 'Australia']
MAX_RESULTS = 500
MAX_CSV_SIZE = 50 * 1024 * 1024  # 50MB

# --- Global State ---
# This dictionary tracks the background scraper's progress in real-time.
SCRAPER_STATUS = {
    "is_running": False,
    "last_updated": "Never",
    "total_jobs_found": 0,
    "current_search": "None",
    "error": None
}
SCRAPER_LOCK = threading.Lock()

# --- Helper Functions ---

def apply_experience_filter(df, exp_level, exp_years):
    """
    Filters the DataFrame based on experience level (Fresher/Experienced).
    Uses Regex to search both Job Title and Description.
    """
    if not exp_level or exp_level == 'Any Experience':
        return df
    
    pattern = ""
    if exp_level == 'fresher':
        # Keywords for Entry Level / Freshers
        pattern = r'\b(fresher|freshers|entry.?level|junior|trainee|intern|graduate|0.? ?[0-2]? ?year?|no experience|recent graduate|202[3-7] ?pass.?out|202[4-8] ?batch|off.?campus|walk.?in|b\.?e\.?|m\.?tech|mca)\b'
    elif exp_level == 'experienced':
        # Keywords for Experienced - use fixed patterns only, never user input
        if exp_years and exp_years.strip():
            # Validate exp_years is numeric only (prevents regex injection)
            exp_years_clean = re.sub(r'[^0-9\-]', '', exp_years.strip())
            if not exp_years_clean:
                # If validation fails, use generic pattern
                pattern = r'\b(senior|lead|manager|architect|experienced|[3-9] ?years?|1[0-9] ?years?)\b'
            else:
                # Only allow safe numeric patterns
                if '-' in exp_years_clean:
                    try:
                        low, high = [x.strip() for x in exp_years_clean.split('-', 1)]
                        pattern = rf'\b({re.escape(low)}|{re.escape(high)})\b.*?year'
                    except:
                        pattern = r'\b(senior|lead|manager|architect|experienced|[3-9] ?years?|1[0-9] ?years?)\b'
                else:
                    pattern = rf'\b{re.escape(exp_years_clean)}\b.*?year'
        else:
            # Generic "experienced" check if no years provided (simple heuristic)
            pattern = r'\b(senior|lead|manager|architect|experienced|[3-9] ?years?|1[0-9] ?years?)\b'

    if not pattern:
        return df

    try:
        # Apply mask to Title OR Description
        # We use 'na=False' to ignore rows where data is missing
        mask = df['title'].str.contains(pattern, case=False, na=False, regex=True) | \
               df['description'].str.contains(pattern, case=False, na=False, regex=True)
        return df[mask]
    except Exception as e:
        # If regex fails, return unfiltered data
        print(f"Regex filter error: {e}")
        return df

def background_scraper(role, location, country, is_remote, results_wanted):
    """
    The worker function that runs in a separate thread.
    """
    global SCRAPER_STATUS
    
    with SCRAPER_LOCK:
        SCRAPER_STATUS["is_running"] = True
        SCRAPER_STATUS["error"] = None
    
    # 1. Smart Search Term Logic
    search_term = role if role else "jobs"
    
    # 2. Site Selection
    sites_to_scrape = ["indeed", "glassdoor", "google"]
    
    print(f"--- Background Scraper Started ---")
    print(f"Search: '{search_term}' | Location: '{location}' | Country: '{country}'")

    try:
        # 3. Run JobSpy
        jobs = scrape_jobs(
            site_name=sites_to_scrape,
            search_term=search_term,
            location=location if not is_remote else None,
            results_wanted=int(results_wanted),
            country_indeed=country,
            is_remote=is_remote,
            linkedin_fetch_description=False
        )

        # 4. Process Results
        if not jobs.empty:
            # Remove duplicate URLs
            jobs = jobs.drop_duplicates(subset='job_url')
            
            # Ensure important columns exist to avoid errors later
            for col in ['title', 'company', 'location', 'description', 'date_posted']:
                if col not in jobs.columns:
                    jobs[col] = 'N/A'

            # Save to CSV
            jobs.to_csv(CSV_FILE, index=False)
            
            # Update Status (thread-safe)
            with SCRAPER_LOCK:
                SCRAPER_STATUS["total_jobs_found"] = len(jobs)
                SCRAPER_STATUS["last_updated"] = datetime.now().strftime("%H:%M:%S")
            print(f"--- Success: Found {len(jobs)} jobs ---")
            
        else:
            with SCRAPER_LOCK:
                SCRAPER_STATUS["error"] = "Scraper finished but found 0 jobs."
            print("--- Finished: 0 Jobs Found ---")

    except Exception as e:
        # Log detailed error but don't expose to users
        print(f"--- Critical Error: {e} ---")
        with SCRAPER_LOCK:
            SCRAPER_STATUS["error"] = "An error occurred during scraping. Please try again later."
        
    finally:
        with SCRAPER_LOCK:
            SCRAPER_STATUS["is_running"] = False

# --- Routes ---

@app.route('/')
def index():
    # Read URL parameters for filtering
    show_all = request.args.get('show_all') == 'true'
    exp_level = request.args.get('exp_level', '')
    exp_years = request.args.get('exp_years', '')
    
    # Input validation
    valid_exp_levels = ['fresher', 'experienced', 'Any Experience', '']
    if exp_level not in valid_exp_levels:
        exp_level = ''
    
    jobs_list = []
    
    # Load data from CSV if it exists
    if os.path.exists(CSV_FILE):
        try:
            # Check file size before reading
            if os.path.getsize(CSV_FILE) > MAX_CSV_SIZE:
                raise ValueError("CSV file is too large")
            
            df = pd.read_csv(CSV_FILE)
            df = df.fillna('N/A')
            
            # Apply Filter if 'show_all' is NOT true and an experience level is selected
            if not show_all and exp_level:
                df = apply_experience_filter(df, exp_level, exp_years)
            
            # Convert to dictionary for HTML template
            jobs_list = df.to_dict('records')
        except Exception as e:
            print(f"Error reading CSV: {e}")
            pass
    
    # Create a copy of status to avoid thread issues
    with SCRAPER_LOCK:
        status_copy = SCRAPER_STATUS.copy()

    return render_template(
        'index.html',
        jobs=jobs_list,
        status=status_copy,
        show_all=show_all,
        current_exp_level=exp_level,
        current_exp_years=exp_years
    )

@app.route('/scrape', methods=['POST'])
def trigger():
    """Validates input and starts the background thread."""
    with SCRAPER_LOCK:
        if SCRAPER_STATUS["is_running"]:
            flash("Scraper is already running. Please wait.")
            return redirect(url_for('index'))

    # 1. Get Form Data
    role = request.form.get('role', '').strip()[:100]  # Limit to 100 chars
    location = request.form.get('location', '').strip()[:100]
    country = request.form.get('country', 'India')
    is_remote = request.form.get('is_remote') == 'on'
    
    # Validate country against whitelist
    if country not in ALLOWED_COUNTRIES:
        country = 'India'
    
    # Validate and cap results_wanted
    try:
        results_wanted = min(int(request.form.get('results_wanted', 20)), MAX_RESULTS)
        results_wanted = max(1, results_wanted)  # At least 1
    except (ValueError, TypeError):
        results_wanted = 20

    # 2. Validation: Require either Role OR Location
    if not role and not location:
        with SCRAPER_LOCK:
            SCRAPER_STATUS["error"] = "Please enter at least a Job Role OR a Location."
        return redirect(url_for('index'))

    # 3. Reset Status (thread-safe)
    with SCRAPER_LOCK:
        SCRAPER_STATUS["total_jobs_found"] = 0
        SCRAPER_STATUS["error"] = None
        SCRAPER_STATUS["current_search"] = f"{role} in {location}"

    # 4. Start Thread
    thread = threading.Thread(target=background_scraper, args=(
        role,
        location,
        country,
        is_remote,
        results_wanted
    ), daemon=True)
    thread.start()
    
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    """Emergency stop button handler."""
    with SCRAPER_LOCK:
        SCRAPER_STATUS["is_running"] = False
        SCRAPER_STATUS["error"] = "Scraper was manually reset by user."
    flash("Scraper status reset.")
    return redirect(url_for('index'))

@app.route('/download')
def download():
    """Allows downloading the current jobs as CSV."""
    if os.path.exists(CSV_FILE):
        # Verify file size before sending
        if os.path.getsize(CSV_FILE) > MAX_CSV_SIZE:
            flash("File is too large to download.")
            return redirect(url_for('index'))
        return send_from_directory('.', CSV_FILE, as_attachment=True, download_name=f"jobs_{datetime.now().date()}.csv")
    return redirect(url_for('index'))

# Add security headers middleware
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    # Run in production mode - debug should be False in production
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, use_reloader=False)
