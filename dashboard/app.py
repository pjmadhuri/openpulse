import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "data/openpulse.db"

st.set_page_config(
    page_title="OpenPulse",
    page_icon="📊",
    layout="wide"
)

connection = sqlite3.connect(DB_PATH)

query = """
SELECT
    r.full_name,
    r.stars,
    r.forks,

    COUNT(DISTINCT i.issue_id) AS total_issues,

    SUM(
        CASE
            WHEN i.state = 'open' THEN 1
            ELSE 0
        END
    ) AS open_issues,

    SUM(
        CASE
            WHEN i.state = 'closed' THEN 1
            ELSE 0
        END
    ) AS closed_issues,

    COUNT(DISTINCT p.pull_request_id) AS total_pull_requests,

    SUM(
        CASE
            WHEN p.state = 'open' THEN 1
            ELSE 0
        END
    ) AS open_pull_requests,

    SUM(
        CASE
            WHEN p.state = 'closed' THEN 1
            ELSE 0
        END
    ) AS closed_pull_requests,

    SUM(
        CASE
            WHEN p.merged_at IS NOT NULL THEN 1
            ELSE 0
        END
    ) AS merged_pull_requests

FROM repositories r

LEFT JOIN issues i
    ON r.repository_id = i.repository_id

LEFT JOIN pull_requests p
    ON r.repository_id = p.repository_id

GROUP BY
    r.repository_id,
    r.full_name,
    r.stars,
    r.forks

ORDER BY r.stars DESC
"""

df = pd.read_sql_query(query, connection)

connection.close()

st.title("📊 OpenPulse")
st.subheader("GitHub Engineering Activity & Project Health Dashboard")

st.write(
    "GitHub repository activity, issues and pull requests "
    "collected through the GitHub REST API."
)

if df.empty:
    st.warning("No data available.")
    st.stop()

# Metrics
total_repositories = len(df)
total_stars = int(df["stars"].sum())
total_issues = int(df["total_issues"].sum())
total_prs = int(df["total_pull_requests"].sum())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Repositories", total_repositories)

with col2:
    st.metric("GitHub Stars", f"{total_stars:,}")

with col3:
    st.metric("Tracked Issues", total_issues)

with col4:
    st.metric("Pull Requests", total_prs)

st.divider()

# Issue activity
st.subheader("Issue Activity by Repository")

issue_chart = df[
    ["full_name", "open_issues", "closed_issues"]
].copy()

issue_chart = issue_chart.set_index("full_name")

issue_chart.columns = [
    "Open Issues",
    "Closed Issues"
]

st.bar_chart(issue_chart)

# PR activity
st.subheader("Pull Request Activity by Repository")

pr_chart = df[
    [
        "full_name",
        "open_pull_requests",
        "closed_pull_requests",
        "merged_pull_requests"
    ]
].copy()

pr_chart = pr_chart.set_index("full_name")

pr_chart.columns = [
    "Open PRs",
    "Closed PRs",
    "Merged PRs"
]

st.bar_chart(pr_chart)

# Repository summary
st.subheader("Repository Health Summary")

display_df = df.copy()

display_df.columns = [
    "Repository",
    "Stars",
    "Forks",
    "Issues",
    "Open Issues",
    "Closed Issues",
    "Pull Requests",
    "Open PRs",
    "Closed PRs",
    "Merged PRs"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Observations
st.subheader("Key Observations")

for _, row in df.iterrows():

    st.write(
        f"**{row['full_name']}** — "
        f"{int(row['total_issues'])} issues and "
        f"{int(row['total_pull_requests'])} pull requests tracked."
    )