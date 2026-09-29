# OpenPulse – GitHub Engineering Activity Pipeline

## Overview

OpenPulse is a small end-to-end Data Engineering project that extracts data from the GitHub REST API, transforms it into structured relational tables, and presents key engineering activity metrics through a Streamlit dashboard.

## What It Does

- Fetches repository, issue, and pull-request data from GitHub
- Handles API pagination, missing fields, retries, and rate-limit monitoring
- Stores raw API responses as JSON
- Loads cleaned data into SQLite
- Models data into:
  - `repositories`
  - `issues`
  - `pull_requests`
- Uses SQL to create reporting metrics such as issue closure and PR activity
- Visualizes the results using Streamlit

## Architecture

GitHub API → Python → Raw JSON → SQLite → SQL Reporting → Streamlit Dashboard

## Repositories

- Apache Airflow
- Apache Spark
- dbt

## Tech Stack

Python | GitHub REST API | SQLite | SQL | Pandas | Streamlit

## Run Locally

```bash
pip install -r requirements.txt
python src/api_client.py
python src/load_data.py
python -m streamlit run dashboard/app.py
