
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

```
