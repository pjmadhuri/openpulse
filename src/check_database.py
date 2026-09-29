import sqlite3

DB_PATH = "data/openpulse.db"


def check_database():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    print("\n==============================")
    print("DATABASE CHECK")
    print("==============================")

    # Repository count
    cursor.execute("""
        SELECT COUNT(*)
        FROM repositories
    """)

    repository_count = cursor.fetchone()[0]

    print(
        f"\nRepositories: {repository_count}"
    )

    # Issue count
    cursor.execute("""
        SELECT COUNT(*)
        FROM issues
    """)

    issue_count = cursor.fetchone()[0]

    print(
        f"Issues: {issue_count}"
    )

    # Pull request count
    cursor.execute("""
        SELECT COUNT(*)
        FROM pull_requests
    """)

    pull_request_count = cursor.fetchone()[0]

    print(
        f"Pull Requests: {pull_request_count}"
    )

    # Repository details
    print("\n------------------------------")
    print("REPOSITORIES")
    print("------------------------------")

    cursor.execute("""
        SELECT
            full_name,
            stars,
            forks,
            open_issues
        FROM repositories
        ORDER BY stars DESC
    """)

    repositories = cursor.fetchall()

    for repository in repositories:

        print(
            f"{repository[0]} | "
            f"Stars: {repository[1]} | "
            f"Forks: {repository[2]} | "
            f"Open Issues: {repository[3]}"
        )

    # Issue count by repository
    print("\n------------------------------")
    print("ISSUES BY REPOSITORY")
    print("------------------------------")

    cursor.execute("""
        SELECT
            r.full_name,
            COUNT(i.issue_id)
        FROM repositories r
        LEFT JOIN issues i
            ON r.repository_id = i.repository_id
        GROUP BY r.full_name
        ORDER BY COUNT(i.issue_id) DESC
    """)

    issue_counts = cursor.fetchall()

    for row in issue_counts:

        print(
            f"{row[0]}: {row[1]} issues"
        )

    # Pull request count by repository
    print("\n------------------------------")
    print("PULL REQUESTS BY REPOSITORY")
    print("------------------------------")

    cursor.execute("""
        SELECT
            r.full_name,
            COUNT(p.pull_request_id)
        FROM repositories r
        LEFT JOIN pull_requests p
            ON r.repository_id = p.repository_id
        GROUP BY r.full_name
        ORDER BY COUNT(p.pull_request_id) DESC
    """)

    pull_request_counts = cursor.fetchall()

    for row in pull_request_counts:

        print(
            f"{row[0]}: {row[1]} pull requests"
        )

    # Check for duplicate issue IDs
    print("\n------------------------------")
    print("DATA QUALITY CHECKS")
    print("------------------------------")

    cursor.execute("""
        SELECT COUNT(*)
        FROM issues
    """)

    total_issue_rows = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT issue_id)
        FROM issues
    """)

    unique_issue_ids = cursor.fetchone()[0]

    print(
        f"Issue duplicate check: "
        f"{total_issue_rows - unique_issue_ids} duplicates"
    )

    # Check duplicate PR IDs
    cursor.execute("""
        SELECT COUNT(*)
        FROM pull_requests
    """)

    total_pr_rows = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(DISTINCT pull_request_id)
        FROM pull_requests
    """)

    unique_pr_ids = cursor.fetchone()[0]

    print(
        f"Pull request duplicate check: "
        f"{total_pr_rows - unique_pr_ids} duplicates"
    )

    connection.close()

    print("\n==============================")
    print("DATABASE CHECK COMPLETE")
    print("==============================")


if __name__ == "__main__":
    check_database()