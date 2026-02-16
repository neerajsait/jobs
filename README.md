

# Unified Job Scraper: Multi-Site Job Search Dashboard

A simple Flask web app that scrapes job listings from multiple sites (Indeed, Glassdoor, Google) using the `jobspy` library, caches results to CSV, and provides basic filtering for fresher/experienced roles. Features real-time status updates, background scraping (no page freeze), and CSV download — built as a personal job search tool.

**Note**: This is a personal/educational prototype. Job scraping may violate some sites' Here is a significantly improved, professional, and portfolio-ready version of your `README.md`.

**Changes made:**

* **Professional Header:** Added a centered layout with a clear tagline and better badge organization.
* **Project Structure:** Added a file tree to help others understand the code layout immediately.
* **"How It Works" Section:** Added a technical breakdown of the background threading and scraping logic (great for recruiters/technical interviews).
* **Polished Instructions:** Fixed the code block formatting and added a "Usage" section.
* **Troubleshooting:** Added a section for common scraping issues (blocking/timeouts).

You can copy-paste the code below directly into your `README.md` file.

---

```markdown
# 🕵️‍♂️ Unified Job Scraper
### A Multi-Site Job Search Dashboard

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-green?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![JobSpy](https://img.shields.io/badge/Powered%20By-JobSpy-orange)](https://github.com/Bunsly/JobSpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **One search to rule them all.** > Stop switching tabs. Search Indeed, Glassdoor, and Google Jobs simultaneously from a single, real-time dashboard.

---

## 📖 Overview

Job hunting is exhausting. Keeping track of listings across multiple platforms (Indeed, Glassdoor, LinkedIn, etc.) often leads to "tab fatigue." 

**Unified Job Scraper** is a personal productivity tool designed to aggregate results into a single view. It runs scrapers in the background to prevent UI freezing, applies smart regex-based filtering to identify "Fresher" vs. "Experienced" roles, and exports clean data to CSV for tracking.

### 🌟 Key Features

* **⚡ Multi-Site Scraping:** Aggregates listings from Indeed, Glassdoor, and Google Jobs in one click.
* **🧵 Non-Blocking UI:** Runs scraping tasks in background threads, providing real-time status updates via the dashboard.
* **🧠 Smart Filtering:** Custom Regex heuristics categorize jobs as **Fresher** (0-2 years) or **Experienced** automatically.
* **🌍 Remote Ready:** Toggle explicitly for remote-only opportunities.
* **💾 Data Persistence:** Results are cached to CSV for offline analysis and record-keeping.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.8+, Flask
* **Scraping Engine:** `jobspy` (lib), `requests`, `BeautifulSoup`
* **Data Processing:** Pandas (Deduplication & Cleaning)
* **Concurrency:** Python `threading` module (Background tasks)
* **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## 📂 Project Structure

```text
unified-job-scraper/
├── app.py              # Main Flask application & routing logic
├── scraper.py          # Background scraping worker & JobSpy integration
├── filters.py          # Regex logic for experience/fresher detection
├── requirements.txt    # Project dependencies
├── static/
│   ├── style.css       # Dashboard styling
│   └── script.js       # Polling logic for status updates
├── templates/
│   ├── index.html      # Search dashboard
│   └── results.html    # Job listing view
└── jobs.csv            # Cached output (auto-generated)

```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* Git

### Installation

1. **Clone the Repository**
```bash
git clone [https://github.com/neerajsait/jobs.git](https://github.com/neerajsait/jobs.git)
cd jobs

```


2. **Create a Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


*(Note: If `requirements.txt` is missing, run: `pip install flask jobspy pandas`)*
4. **Run the Application**
```bash
python app.py

```


5. **Access the Dashboard**
Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 💡 How It Works

1. **The Request:** The user submits a job role (e.g., "Python Developer") and location via the web form.
2. **The Thread:** Flask starts a background thread using Python's `threading` module so the web page doesn't freeze while scraping.
3. **The Scrape:** The app utilizes `jobspy` to query selected providers (Indeed, Glassdoor, etc.).
4. **The Filter:** Raw results are passed through a Pandas DataFrame where regex patterns filter out irrelevant experience levels based on user preference.
5. **The Response:** The frontend polls the backend for status updates and renders the final table once the thread completes.

---

## 📸 Screenshots

| Dashboard View | Results Table |
| --- | --- |
| *[Place Screenshot Here]* | *[Place Screenshot Here]* |
| *Clean search interface* | *Filtered & sorted results* |

---

## ⚠️ Known Issues & Limitations

* **Rate Limiting:** If you search too frequently, sites like Indeed may temporarily block your IP. Using a VPN can help.
* **LinkedIn Blocking:** LinkedIn scraping is currently disabled by default in the code as they have very aggressive anti-bot measures.
* **False Positives:** The "Fresher" filter uses keyword matching (e.g., "0-1 years", "Entry Level"). It may occasionally miss-categorize vaguely worded job descriptions.

---

## 🗺️ Roadmap

* [ ] **Email Alerts:** Send daily summaries of new matches.
* [ ] **Proxy Rotation:** Integrate reliable proxy support to avoid 429 errors.
* [ ] **Salary Parsing:** Extract and normalize salary ranges for better sorting.
* [ ] **Docker Support:** Containerize the app for easy deployment.

---

## ⚖️ Legal & Ethical Disclaimer

**Strictly for Educational and Personal Use Only.**

Web scraping exists in a legal gray area. This tool is intended to automate the user's *own* manual search process.

* **Do not** use this tool for commercial data mining.
* **Do not** overload servers with high-frequency requests.
* **Respect** the `robots.txt` of the target websites.

*The author is not responsible for any misuse of this tool or potential account bans resulting from excessive scraping.*

---

## 🤝 Contributing

Contributions are welcome! If you have a fix for a broken scraper or a better filtering regex, feel free to fork and submit a PR.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

```

```Terms of Service — use responsibly and only for non-commercial, personal purposes.

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


