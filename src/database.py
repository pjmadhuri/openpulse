import sqlite3

DB_PATH = "data/openpulse.db"


def create_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Repository table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS repositories (
            repository_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            owner TEXT,
            name TEXT,
            description TEXT,
            language TEXT,
            stars INTEGER,
            forks INTEGER,
            open_issues INTEGER,
            created_at TEXT,
            updated_at TEXT,
            ingested_at TEXT
        )
    """)

    # Issues table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            issue_id INTEGER PRIMARY KEY,
            repository_id INTEGER,
            issue_number INTEGER,
            title TEXT,
            state TEXT,
            author TEXT,
            created_at TEXT,
            updated_at TEXT,
            closed_at TEXT,
            comments INTEGER,
            ingested_at TEXT,
            FOREIGN KEY (repository_id)
                REFERENCES repositories(repository_id)
        )
    """)

    # Pull requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pull_requests (
            pull_request_id INTEGER PRIMARY KEY,
            repository_id INTEGER,
            pr_number INTEGER,
            title TEXT,
            state TEXT,
            author TEXT,
            created_at TEXT,
            updated_at TEXT,
            closed_at TEXT,
            merged_at TEXT,
            comments INTEGER,
            ingested_at TEXT,
            FOREIGN KEY (repository_id)
                REFERENCES repositories(repository_id)
        )
    """)

    connection.commit()
    connection.close()

    print("SQLite database and tables created successfully.")


if __name__ == "__main__":
    create_database()