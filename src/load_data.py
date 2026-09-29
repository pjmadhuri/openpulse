import json
import sqlite3
from datetime import datetime, timezone

DB_PATH = "data/openpulse.db"
JSON_PATH = "data/raw_github_data.json"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_repositories(connection, all_data):
    cursor = connection.cursor()

    for data in all_data:

        repository = data["repository"]

        cursor.execute("""
            INSERT OR REPLACE INTO repositories (
                repository_id,
                full_name,
                owner,
                name,
                description,
                language,
                stars,
                forks,
                open_issues,
                created_at,
                updated_at,
                ingested_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            repository.get("id"),
            repository.get("full_name"),
            repository.get("owner", {}).get("login"),
            repository.get("name"),
            repository.get("description"),
            repository.get("language"),
            repository.get("stargazers_count"),
            repository.get("forks_count"),
            repository.get("open_issues_count"),
            repository.get("created_at"),
            repository.get("updated_at"),
            datetime.now(timezone.utc).isoformat()
        ))

    print(
        f"Repositories loaded: {len(all_data)}"
    )


def load_issues(connection, all_data):
    cursor = connection.cursor()

    total_issues = 0

    for data in all_data:

        repository = data["repository"]
        repository_id = repository["id"]

        for issue in data["issues"]:

            author = None

            if issue.get("user"):
                author = issue["user"].get("login")

            cursor.execute("""
                INSERT OR REPLACE INTO issues (
                    issue_id,
                    repository_id,
                    issue_number,
                    title,
                    state,
                    author,
                    created_at,
                    updated_at,
                    closed_at,
                    comments,
                    ingested_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                issue.get("id"),
                repository_id,
                issue.get("number"),
                issue.get("title"),
                issue.get("state"),
                author,
                issue.get("created_at"),
                issue.get("updated_at"),
                issue.get("closed_at"),
                issue.get("comments", 0),
                datetime.now(timezone.utc).isoformat()
            ))

            total_issues += 1

    print(
        f"Issues loaded: {total_issues}"
    )


def load_pull_requests(connection, all_data):
    cursor = connection.cursor()

    total_pull_requests = 0

    for data in all_data:

        repository = data["repository"]
        repository_id = repository["id"]

        for pull_request in data["pull_requests"]:

            author = None

            if pull_request.get("user"):
                author = pull_request["user"].get("login")

            cursor.execute("""
                INSERT OR REPLACE INTO pull_requests (
                    pull_request_id,
                    repository_id,
                    pr_number,
                    title,
                    state,
                    author,
                    created_at,
                    updated_at,
                    closed_at,
                    merged_at,
                    comments,
                    ingested_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pull_request.get("id"),
                repository_id,
                pull_request.get("number"),
                pull_request.get("title"),
                pull_request.get("state"),
                author,
                pull_request.get("created_at"),
                pull_request.get("updated_at"),
                pull_request.get("closed_at"),
                pull_request.get("merged_at"),
                pull_request.get("comments", 0),
                datetime.now(timezone.utc).isoformat()
            ))

            total_pull_requests += 1

    print(
        f"Pull requests loaded: "
        f"{total_pull_requests}"
    )


def load_data():

    # Read raw API data
    with open(
        JSON_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        all_data = json.load(file)

    print(
        f"Repositories found in JSON: "
        f"{len(all_data)}"
    )

    connection = get_connection()

    try:

        load_repositories(
            connection,
            all_data
        )

        load_issues(
            connection,
            all_data
        )

        load_pull_requests(
            connection,
            all_data
        )

        connection.commit()

        print("\nData loading completed successfully.")

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


if __name__ == "__main__":
    load_data()