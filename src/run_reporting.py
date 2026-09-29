import sqlite3
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "openpulse.db"
)

SQL_PATH = os.path.join(
    BASE_DIR,
    "sql",
    "reporting.sql"
)


def run_reporting():

    print("Database:")
    print(DB_PATH)

    print("\nSQL file:")
    print(SQL_PATH)

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    with open(
        SQL_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        sql_script = file.read()

    print("\nExecuting reporting SQL...")

    cursor.executescript(sql_script)

    connection.commit()

    print("Reporting layer created successfully.")

    # Verify the actual columns
    print("\nColumns in repo_health_summary:")

    cursor.execute("""
        PRAGMA table_info(repo_health_summary)
    """)

    columns = cursor.fetchall()

    for column in columns:
        print("-", column[1])

    connection.close()


if __name__ == "__main__":
    run_reporting()