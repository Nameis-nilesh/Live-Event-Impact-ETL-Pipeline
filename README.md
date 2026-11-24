# 🎟️ Live Event Impact ETL Pipeline

<p align="center">
  <strong>Turning live-event data into measurable artist-impact insights.</strong><br/>
  An end-to-end Python ETL project that combines event information with Spotify artist metrics and stores structured snapshots in MySQL.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white" alt="Python 3.9+"/>
  <img src="https://img.shields.io/badge/ETL-Data%20Engineering-0A7B83" alt="ETL"/>
  <img src="https://img.shields.io/badge/Database-MySQL-4479A1?logo=mysql&logoColor=white" alt="MySQL"/>
  <img src="https://img.shields.io/badge/API-Spotify-1DB954?logo=spotify&logoColor=white" alt="Spotify API"/>
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License"/>
</p>

---

## 📌 Project overview

**Live Event Impact ETL Pipeline** is a data-engineering project designed to bring event information and artist popularity signals together in one analytical dataset.

The pipeline collects event details, enriches artist records with Spotify data, and loads the results into a MySQL database. The stored data can support analysis of artist visibility and audience interest around live events.

> **Project focus:** web data extraction → API enrichment → transformation → relational storage → analytical querying.

## 🎯 Goals

- Collect event information such as artist, event date, city, and event details.
- Enrich artist records using the Spotify Web API.
- Capture available artist metrics, including follower count and popularity.
- Retrieve popular-track information for additional artist-level context.
- Store event records and dated artist metric snapshots in MySQL.
- Keep the workflow organized into reusable Python modules.

## 🧭 Pipeline architecture

~~~mermaid
flowchart TD
    A[Event listing source] --> B[Web scraper]
    B --> C[Clean and normalize event data]
    C --> D[Spotify API enrichment]
    D --> E[Artist and track metrics]
    E --> F[MySQL database]
    F --> G[Dim_Events]
    F --> H[Fact_Artist_Daily_Metrics]
    G --> I[SQL analysis and reporting]
    H --> I
~~~

### ETL workflow

| Stage | What happens |
|---|---|
| **Extract** | The scraper requests an event page and parses event-card information. |
| **Transform** | Event fields are organized, dates are normalized, and artist names are used to look up Spotify profiles. |
| **Enrich** | Spotify artist information and popular-track details are collected where available. |
| **Load** | Event details and dated artist metric records are inserted or updated in MySQL. |
| **Analyze** | SQL queries can explore event coverage and changes in artist metrics over repeated runs. |

## 🛠️ Technology stack

| Technology | Role |
|---|---|
| **Python** | Pipeline orchestration and data processing |
| **Pandas** | Tabular data handling and date transformation |
| **Requests** | HTTP requests to event pages |
| **Beautiful Soup 4** | HTML parsing and event extraction |
| **Spotipy** | Spotify Web API integration |
| **MySQL** | Relational storage for event and artist metric data |
| **mysql-connector-python** | Python-to-MySQL connectivity |
| **Jupyter Notebook** | Exploration and experimentation |

## 📁 Repository structure

The current Python application is inside the nested Spotify directory:

~~~text
Live-Event-Impact-ETL-Pipeline/
├── README.md
├── LICENSE
└── Live-Event-Impact-ETL-Pipeline-main/
    └── Live-Event-Impact-ETL-Pipeline-main/
        └── Spotify/
            ├── config.py
            ├── database.py
            ├── main.py
            ├── scraper.py
            ├── spotify_client.py
            └── spotify project.ipynb
~~~

### Module responsibilities

| File | Responsibility |
|---|---|
| **main.py** | Coordinates the scraper, Spotify enrichment, database inserts, and pipeline shutdown. |
| **scraper.py** | Requests and parses event listing pages; prepares event data for the pipeline. |
| **spotify_client.py** | Connects to Spotify and retrieves artist information and popular tracks. |
| **database.py** | Creates database connections and handles event and daily-metric persistence. |
| **config.py** | Holds local connection and API configuration. Keep this file private; never commit credentials. |
| **spotify project.ipynb** | Notebook for exploration and project experimentation. |

## 🗃️ Database design

The application writes to two MySQL tables:

### 1. Dim_Events

Stores event-level information, including the artist, event date, and city. This table supports questions such as:

- Which artists have events in a particular city?
- How many events are scheduled in a selected period?
- Which artists appear across multiple event listings?

### 2. Fact_Artist_Daily_Metrics

Stores dated artist metric observations, including the Spotify artist identifier and the metrics returned by the API. Keeping a snapshot date makes it possible to compare observations across multiple pipeline runs.

**Recommended keys:** use a unique key on (Artist_Name, City, Event_Date) in Dim_Events, and on (Spotify_Artist_ID, Snapshot_Date) in Fact_Artist_Daily_Metrics. These keys support the project's insert-or-update approach and help prevent duplicate records. Adapt column names and types to match the SQL statements in database.py.

## ⚙️ Getting started

### Prerequisites

- Python 3.9 or newer
- MySQL Server
- A Spotify Developer application with a Client ID and Client Secret
- Git

### 1. Clone the repository

~~~bash
git clone https://github.com/Nameis-nilesh/Live-Event-Impact-ETL-Pipeline.git
cd Live-Event-Impact-ETL-Pipeline
~~~

### 2. Open the project directory

~~~bash
cd Live-Event-Impact-ETL-Pipeline-main/Live-Event-Impact-ETL-Pipeline-main/Spotify
~~~

### 3. Create and activate a virtual environment

**Windows (PowerShell):**

~~~powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
~~~

**macOS / Linux:**

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

### 4. Install dependencies

~~~bash
pip install pandas requests beautifulsoup4 spotipy mysql-connector-python
~~~

### 5. Create the MySQL database

Open MySQL Workbench or a MySQL client and run:

~~~sql
CREATE DATABASE eventimpactdb;
~~~

The Python database module expects the database to exist and writes to Dim_Events and Fact_Artist_Daily_Metrics. Create those tables using the column definitions and insert statements in database.py before running the pipeline. Add the recommended unique keys described in the Database design section, ensuring the key columns match the actual schema.

### 6. Configure credentials securely

Set your Spotify application credentials and MySQL connection details in your **local-only** configuration. The current code reads configuration from config.py.

**Important security note:** do not publish Spotify secrets, database passwords, access tokens, or other credentials. If a credential has ever been committed to Git, treat it as exposed: rotate it with the provider, remove it from the tracked source, and use environment variables or a private local configuration going forward. Adding a secret to .gitignore does not erase it from earlier Git history.

A safer future configuration pattern is to read values from environment variables and provide a committed config.example.py containing placeholders only.

### 7. Run the pipeline

~~~bash
python main.py
~~~

The main script coordinates the event extraction, Spotify lookup, and database loading stages. Review the terminal output and MySQL tables to verify the run.

## 🔎 Example SQL analysis

Once the tables contain data, you can start exploring the results. Adjust field names to match the schema defined in database.py.

**Events by city**

~~~sql
SELECT
    City,
    COUNT(*) AS total_events
FROM Dim_Events
GROUP BY City
ORDER BY total_events DESC;
~~~

**Artists with the most listed events**

~~~sql
SELECT
    Artist_Name,
    COUNT(*) AS event_count
FROM Dim_Events
GROUP BY Artist_Name
ORDER BY event_count DESC
LIMIT 10;
~~~

**Daily artist metric history**

~~~sql
SELECT
    Spotify_Artist_ID,
    Snapshot_Date,
    Followers,
    Popularity
FROM Fact_Artist_Daily_Metrics
ORDER BY Spotify_Artist_ID, Snapshot_Date;
~~~

These queries are starting points for analysis. Exact metric column names should follow the table definitions in your local database code.

## 🧪 Data quality and operational notes

- **Scraper selectors:** the scraper relies on page-specific HTML/CSS selectors. If the event website changes its markup, update the selectors in scraper.py.
- **Source configuration:** the scraper's URL is optional in the current implementation. Configure a real event-listing URL and confirm that the page structure matches the parser before relying on live results.
- **Seed data fallback:** when no URL is configured or scraping returns no usable records, the current scraper can fall back to a small set of hard-coded sample events. Treat these as sample data, not verified live listings.
- **API matching:** artist-name searches can return ambiguous matches. Validate artist identity when accuracy is important.
- **API availability:** returned fields and endpoint behavior depend on Spotify's current API access and application permissions.
- **Historical trends:** daily metrics become a time series only after the pipeline is run on multiple dates and snapshots are retained.
- **Idempotency:** database uniqueness constraints should align with the project's insert-or-update logic to avoid duplicate event and snapshot records.

## 🚀 Future improvements

- [ ] Move secrets and connection settings to environment variables.
- [ ] Add a requirements.txt for reproducible dependency installation.
- [ ] Add SQL schema/setup scripts so the database can be initialized in one step.
- [ ] Add structured logging and clearer error handling for network, API, and database failures.
- [ ] Add retries, request timeouts, and rate-limit handling.
- [ ] Validate scraped records and handle missing or malformed dates.
- [ ] Add automated tests for parsing, transformations, and database operations.
- [ ] Schedule daily runs to build a reliable artist-metric history.
- [ ] Build a Power BI or Tableau dashboard for event and artist-impact analysis.

## 💡 Skills demonstrated

**Python · ETL Pipelines · Web Scraping · REST API Integration · Data Cleaning · Pandas · SQL · MySQL · Database Design · Data Engineering**

## 👤 Author

**Nilesh Yadav**

- GitHub: [@Nameis-nilesh](https://github.com/Nameis-nilesh)
- Repository: [Live-Event-Impact-ETL-Pipeline](https://github.com/Nameis-nilesh/Live-Event-Impact-ETL-Pipeline)

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  If you find this project useful, consider giving the repository a ⭐
</p>
