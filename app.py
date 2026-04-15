import threading
import pandas as pd
import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.exceptions import BadRequest
from jobspy import scrape_jobs
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Security configs
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

CSV_FILE = 'jobs_cache.csv'
ALLOWED_COUNTRIES = ['USA', 'India', 'UK', 'Canada', 'Australia']
MAX_RESULTS = 500
MAX_CSV_SIZE = 50 * 1024 * 1024  # 50MB

SCRAPER_STATUS = {
    "is_running": False,
    "last_updated": "Never",
    "total_jobs_found": 0,
    "current_search": "None",
    "error": None
}

SCRAPER_LOCK = threading.Lock()

# -----------------------------
# Experience Filter
# -----------------------------
def apply_experience_filter(df, exp_level, exp_years):
    if not exp_level or exp_level == 'Any Experience':
        return df

    pattern = ""

    if exp_level == 'fresher':
        pattern = r'\b(fresher|freshers|entry.?level|junior|trainee|intern|graduate|0.? ?[0-2]? ?year?|no experience)\b'

    elif exp_level == 'experienced':
        if exp_years and exp_years.strip():
            exp_years_clean = re.sub(r'[^0-9\-]', '', exp_years.strip())

            if not exp_years_clean:
                pattern = r'\b(senior|lead|manager|architect|experienced|[3-9] ?years?|1[0-9] ?years?)\b'
            else:
                if '-' in exp_years_clean:
                    try:
                        low, high = exp_years_clean.split('-', 1)
                        pattern = rf'\b({re.escape(low)}|{re.escape(high)})\b.*?year'
                    except:
                        pattern = r'\b(senior|lead|manager|architect|experienced)\b'
                else:
                    pattern = rf'\b{re.escape(exp_years_clean)}\b.*?year'
        else:
            pattern = r'\b(senior|lead|manager|architect|experienced|[3-9] ?years?)\b'

    if not pattern:
        return df

    try:
        mask = df['title'].str.contains(pattern, case=False, na=False, regex=True) | \
               df['description'].str.contains(pattern, case=False, na=False, regex=True)
        return df[mask]
    except Exception as e:
        print(f"Regex error: {e}")
        return df


# -----------------------------
# Background Scraper
# -----------------------------
def background_scraper(role, location, country, is_remote, results_wanted):
    global SCRAPER_STATUS

    with SCRAPER_LOCK:
        SCRAPER_STATUS["is_running"] = True
        SCRAPER_STATUS["error"] = None

    search_term = role if role else "jobs"
    sites_to_scrape = ["indeed", "glassdoor", "google"]

    try:
        jobs = scrape_jobs(
            site_name=sites_to_scrape,
            search_term=search_term,
            location=location if not is_remote else None,
            results_wanted=int(results_wanted),
            country_indeed=country,
            is_remote=is_remote,
            linkedin_fetch_description=False
        )

        if not jobs.empty:
            jobs = jobs.drop_duplicates(subset='job_url')

            for col in ['title', 'company', 'location', 'description', 'date_posted']:
                if col not in jobs.columns:
                    jobs[col] = 'N/A'

            jobs.to_csv(CSV_FILE, index=False)

            with SCRAPER_LOCK:
                SCRAPER_STATUS["total_jobs_found"] = len(jobs)
                SCRAPER_STATUS["last_updated"] = datetime.now().strftime("%H:%M:%S")

        else:
            with SCRAPER_LOCK:
                SCRAPER_STATUS["error"] = "No jobs found."

    except Exception as e:
        print(f"Scraper error: {e}")
        with SCRAPER_LOCK:
            SCRAPER_STATUS["error"] = "Scraping failed."

    finally:
        with SCRAPER_LOCK:
            SCRAPER_STATUS["is_running"] = False


# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    show_all = request.args.get('show_all') == 'true'
    exp_level = request.args.get('exp_level', '')
    exp_years = request.args.get('exp_years', '')

    jobs_list = []

    if os.path.exists(CSV_FILE):
        try:
            if os.path.getsize(CSV_FILE) > MAX_CSV_SIZE:
                raise ValueError("CSV too large")

            df = pd.read_csv(CSV_FILE).fillna('N/A')

            if not show_all and exp_level:
                df = apply_experience_filter(df, exp_level, exp_years)

            jobs_list = df.to_dict('records')

        except Exception as e:
            print(f"CSV error: {e}")

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
    with SCRAPER_LOCK:
        if SCRAPER_STATUS["is_running"]:
            flash("Scraper already running.")
            return redirect(url_for('index'))

    role = request.form.get('role', '').strip()[:100]
    location = request.form.get('location', '').strip()[:100]
    country = request.form.get('country', 'India')
    is_remote = request.form.get('is_remote') == 'on'

    if country not in ALLOWED_COUNTRIES:
        country = 'India'

    try:
        results_wanted = min(int(request.form.get('results_wanted', 20)), MAX_RESULTS)
        results_wanted = max(1, results_wanted)
    except:
        results_wanted = 20

    if not role and not location:
        flash("Enter role or location.")
        return redirect(url_for('index'))

    with SCRAPER_LOCK:
        SCRAPER_STATUS["total_jobs_found"] = 0
        SCRAPER_STATUS["error"] = None
        SCRAPER_STATUS["current_search"] = f"{role} in {location}"

    thread = threading.Thread(
        target=background_scraper,
        args=(role, location, country, is_remote, results_wanted),
        daemon=True
    )
    thread.start()

    return redirect(url_for('index'))


@app.route('/download')
def download():
    if os.path.exists(CSV_FILE):
        if os.path.getsize(CSV_FILE) > MAX_CSV_SIZE:
            flash("File too large.")
            return redirect(url_for('index'))

        return send_from_directory(
            '.', CSV_FILE,
            as_attachment=True,
            download_name=f"jobs_{datetime.now().date()}.csv"
        )

    return redirect(url_for('index'))


# -----------------------------
# Security Headers
# -----------------------------
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, use_reloader=False)