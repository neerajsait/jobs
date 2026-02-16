import threading
import pandas as pd
import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from jobspy import scrape_jobs
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'unified_scraper_secret_key'

# --- Configuration ---
CSV_FILE = 'jobs_cache.csv'

# --- Global State ---
# This dictionary tracks the background scraper's progress in real-time.
SCRAPER_STATUS = {
    "is_running": False,
    "last_updated": "Never",
    "total_jobs_found": 0,
    "current_search": "None",
    "error": None
}

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
        # Keywords for Experienced
        if exp_years and exp_years.strip():
            # If user provided specific years (e.g. "3-5"), build a dynamic regex
            exp_years = exp_years.strip()
            if '-' in exp_years:
                try:
                    low, high = [x.strip() for x in exp_years.split('-', 1)]
                    pattern = rf'\b({low}|{high})\b.*?year|experience.*?({low}.*?{high})'
                except:
                    pattern = rf'\b{exp_years}\b.*?year' # Fallback
            else:
                pattern = rf'\b{exp_years}\b.*?year'
        else:
            # Generic "experienced" check if no years provided (simple heuristic)
            pattern = r'\b(senior|lead|manager|architect|experienced|[3-9] ?years?|1[0-9] ?years?)\b'

    if not pattern:
        return df

    # Apply mask to Title OR Description
    # We use 'na=False' to ignore rows where data is missing
    mask = df['title'].str.contains(pattern, case=False, na=False, regex=True) | \
           df['description'].str.contains(pattern, case=False, na=False, regex=True)
    
    return df[mask]

def background_scraper(role, location, country, is_remote, results_wanted):
    """
    The worker function that runs in a separate thread.
    """
    global SCRAPER_STATUS
    SCRAPER_STATUS["is_running"] = True
    SCRAPER_STATUS["error"] = None
    
    # 1. Smart Search Term Logic
    # If Role is empty, use a generic term like "hiring" or "jobs" so the scraper has something to search.
    search_term = role if role else "jobs"
    
    # 2. Site Selection
    # LinkedIn is removed by default for stability (it blocks often). 
    # Add it back to the list ["indeed", "glassdoor", "google", "linkedin"] if you want to risk it.
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
            country_indeed=country if country in ["USA", "India", "UK"] else "India",
            is_remote=is_remote,
            linkedin_fetch_description=False  # Set True if you need full descriptions (slower)
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
            
            # Update Status
            SCRAPER_STATUS["total_jobs_found"] = len(jobs)
            SCRAPER_STATUS["last_updated"] = datetime.now().strftime("%H:%M:%S")
            print(f"--- Success: Found {len(jobs)} jobs ---")
            
        else:
            SCRAPER_STATUS["error"] = f"Scraper finished but found 0 jobs for '{search_term}'."
            print("--- Finished: 0 Jobs Found ---")

    except Exception as e:
        print(f"--- Critical Error: {e} ---")
        SCRAPER_STATUS["error"] = str(e)
        
    finally:
        SCRAPER_STATUS["is_running"] = False

# --- Routes ---

@app.route('/')
def index():
    # Read URL parameters for filtering
    show_all = request.args.get('show_all') == 'true'
    exp_level = request.args.get('exp_level', '')
    exp_years = request.args.get('exp_years', '')
    
    jobs_list = []
    
    # Load data from CSV if it exists
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df = df.fillna('N/A') # Fill missing values
            
            # Apply Filter if 'show_all' is NOT true and an experience level is selected
            if not show_all and exp_level:
                df = apply_experience_filter(df, exp_level, exp_years)
            
            # Convert to dictionary for HTML template
            jobs_list = df.to_dict('records')
        except Exception as e:
            print(f"Error reading CSV: {e}")
            # If CSV is corrupt, we just return empty list
            pass

    return render_template(
        'index.html',
        jobs=jobs_list,
        status=SCRAPER_STATUS,
        show_all=show_all,
        # Pass current filter params back to template so inputs stay filled
        current_exp_level=exp_level,
        current_exp_years=exp_years
    )

@app.route('/scrape', methods=['POST'])
def trigger():
    """Validates input and starts the background thread."""
    if SCRAPER_STATUS["is_running"]:
        flash("Scraper is already running. Please wait.")
        return redirect(url_for('index'))

    # 1. Get Form Data
    role = request.form.get('role', '').strip()
    location = request.form.get('location', '').strip()
    country = request.form.get('country', 'India') # Default to India
    is_remote = request.form.get('is_remote') == 'on'
    results_wanted = request.form.get('results_wanted', 20)

    # 2. Validation: Require either Role OR Location
    if not role and not location:
        SCRAPER_STATUS["error"] = "Validation Error: Please enter at least a Job Role OR a Location."
        return redirect(url_for('index'))

    # 3. Reset Status
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
    ))
    thread.start()
    
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    """Emergency stop button handler."""
    global SCRAPER_STATUS
    SCRAPER_STATUS["is_running"] = False
    SCRAPER_STATUS["error"] = "Scraper was manually reset by user."
    flash("Scraper status reset.")
    return redirect(url_for('index'))

@app.route('/download')
def download():
    """Allows downloading the current jobs as CSV."""
    if os.path.exists(CSV_FILE):
        return send_from_directory('.', CSV_FILE, as_attachment=True, download_name=f"jobs_{datetime.now().date()}.csv")
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Threaded mode enabled for better performance
    app.run(debug=True, use_reloader=False)