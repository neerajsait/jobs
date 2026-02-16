markdown

# Unified Job Scraper: Multi-Site Job Search Dashboard

A simple Flask web app that scrapes job listings from multiple sites (Indeed, Glassdoor, Google) using the `jobspy` library, caches results to CSV, and provides basic filtering for fresher/experienced roles. Features real-time status updates, background scraping (no page freeze), and CSV download — built as a personal job search tool.

**Note**: This is a personal/educational prototype. Job scraping may violate some sites' Terms of Service — use responsibly and only for non-commercial, personal purposes.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-green)](https://flask.palletsprojects.com/)
[![JobSpy](https://img.shields.io/badge/JobSpy-Scraper-orange)](https://github.com/Bunsly/JobSpy)
[![License](https://img.shields.io/badge/License-MIT-yellowgreen)](LICENSE)
[![Commits](https://img.shields.io/github/commit-activity/m/neerajsait/jobs)](https://github.com/neerajsait/jobs/commits/main)

## Why I Built This
Job hunting can be exhausting — searching the same role across Indeed, Glassdoor, LinkedIn, etc., one tab at a time. I wanted a single dashboard where I could enter a role/location once and get combined results quickly.

This started as a free-time project to help with my own job search (mostly full-stack/Java roles in India). I added fresher/experienced filtering because many postings don't explicitly state experience level, and regex heuristics help surface relevant ones. Background threading and status updates were added to make it feel responsive. It's still basic, but it's already saved me hours.

## Key Features
- **Multi-Site Scraping** → Indeed + Glassdoor + Google Jobs (LinkedIn optional but disabled by default due to blocking)
- **Background Scraping** → Runs in a separate thread with live status (no frozen browser)
- **Smart Experience Filtering** → Regex-based filter for "Fresher" (entry-level, 0-2 years, recent grads) or "Experienced" (with optional years like "3-5")
- **Remote Job Support** → Toggle for remote-only results
- **CSV Cache & Download** → Results saved locally and downloadable with timestamp
- **Simple Dashboard** → Real-time progress, error messages, and filtered job list

## Screenshots
*(Add these to make it pop! Run the app locally, trigger a scrape, filter results, and screenshot the dashboard/status/download. Upload to `/screenshots` folder.)*

<!-- Example placeholders — replace with real ones -->
<!-- ![Dashboard](screenshots/dashboard.png) -->
<!-- ![Scraping Status](screenshots/status.png) -->
<!-- ![Filtered Results](screenshots/filtered.png) -->
<!-- ![CSV Download](screenshots/download.png) -->

## Tech Stack
- **Backend** — Python 3.8+ with Flask
- **Scraper** — [jobspy](https://github.com/Bunsly/JobSpy)
- **Data Handling** — Pandas (for filtering/deduping)
- **Threading** — Built-in Python threading for background tasks

## Installation & Setup
### Prerequisites
- Python 3.8+
- (Optional) Proxy/VPN if you hit rate limits

### Steps
1. Clone the repo
   ```bash
   git clone https://github.com/neerajsait/jobs.git
   cd jobs

Create virtual environment (recommended)bash

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

Install dependenciesbash

pip install flask jobspy pandas

Run the appbash

python app.py

Open in browser
Visit http://127.0.0.1:5000Enter a role (or leave blank for broad search), location, toggle options, and click "Start Scraping".

What I Learned & Challengesjobspy is powerful but fragile — sites change often, and LinkedIn blocks aggressively, so I disabled it by default.
Threading in Flask was new; had to be careful with global status dict and avoid race conditions.
Building good regex for experience filtering was tricky — false positives/negatives are common, but the heuristics work decently for Indian job postings.
Learned how to keep the UI responsive during long-running tasks.

Future ImprovementsRe-enable LinkedIn safely (with delays/proxies)
Add more filters (salary, company, date posted)
Pagination and better UI (maybe React frontend)
Email alerts for new matches
Deploy to Render/Vercel for live access
Cache expiration and auto-refresh

Important Ethics & Legal NoteFor personal and educational use only.Many job sites prohibit automated scraping in their Terms of Service.
This tool is meant for light, personal job searching — do not abuse it or run at high volume.
Respect robots.txt and rate limits.
I am not responsible for any account bans or legal issues from misuse.


Add screenshots soon — a live dashboard with real job results will make this repo stand out a lot. Among your projects, this one feels the most "useful tool" rather than pure experiment, which is great for a portfolio. Keep building!

