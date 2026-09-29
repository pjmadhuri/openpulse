import requests
import json
import time

BASE_URL = "https://api.github.com"

REPOSITORIES = [
    ("apache", "airflow"),
    ("apache", "spark"),
    ("dbt-labs", "dbt-core")
]


def make_request(url, params=None, retries=3):
    """
    Make a GitHub API request with basic retry handling.
    Handles temporary API errors and rate-limit responses.
    """

    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=10
            )

            remaining = response.headers.get("X-RateLimit-Remaining")

            print(
                f"Status: {response.status_code} | "
                f"Rate limit remaining: {remaining}"
            )

            if response.status_code == 200:
                return response.json()

            # Retry temporary errors
            if response.status_code in [429, 500, 502, 503, 504]:
                wait_time = 2 ** attempt

                print(
                    f"Temporary API error. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)
                continue

            response.raise_for_status()

        except requests.exceptions.RequestException as error:

            print(f"Request error: {error}")

            if attempt < retries - 1:
                wait_time = 2 ** attempt

                print(
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                raise

    raise Exception("API request failed after retries.")


def get_repository(owner, repo):
    """
    Fetch repository metadata.
    """

    url = f"{BASE_URL}/repos/{owner}/{repo}"

    return make_request(url)


def get_paginated_data(
    owner,
    repo,
    endpoint,
    pages=3,
    per_page=30
):
    """
    Fetch data from a paginated GitHub endpoint.
    """

    all_records = []

    url = f"{BASE_URL}/repos/{owner}/{repo}/{endpoint}"

    for page in range(1, pages + 1):

        print(
            f"Fetching {endpoint} | "
            f"{owner}/{repo} | "
            f"Page {page}"
        )

        params = {
            "page": page,
            "per_page": per_page,
            "state": "all"
        }

        records = make_request(
            url,
            params=params
        )

        if not records:
            break

        all_records.extend(records)

    return all_records


def collect_repository_data(owner, repo):
    """
    Collect repository metadata,
    issues and pull requests.
    """

    print("\n====================================")
    print(f"Repository: {owner}/{repo}")
    print("====================================")

    # Repository metadata
    repository = get_repository(owner, repo)

    # GitHub /issues endpoint can contain both
    # issues and pull requests.
    issue_records = get_paginated_data(
        owner,
        repo,
        "issues",
        pages=3,
        per_page=30
    )

    # Keep only actual issues.
    # Pull requests contain a "pull_request" field.
    issues = [
        issue
        for issue in issue_records
        if "pull_request" not in issue
    ]

    # Fetch pull requests separately.
    pull_requests = get_paginated_data(
        owner,
        repo,
        "pulls",
        pages=3,
        per_page=30
    )

    print(
        f"Actual issues collected: {len(issues)}"
    )

    print(
        f"Pull requests collected: "
        f"{len(pull_requests)}"
    )

    return {
        "repository": repository,
        "issues": issues,
        "pull_requests": pull_requests
    }


if __name__ == "__main__":

    all_data = []

    for owner, repo in REPOSITORIES:

        data = collect_repository_data(
            owner,
            repo
        )

        all_data.append(data)

    # Save raw API response
    with open(
        "data/raw_github_data.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_data,
            file,
            indent=2
        )

    print("\n====================================")
    print("INGESTION COMPLETE")
    print("====================================")

    for data in all_data:

        repository = data["repository"]["full_name"]

        issues_count = len(data["issues"])

        pull_requests_count = len(
            data["pull_requests"]
        )

        print(
            f"{repository}: "
            f"{issues_count} issues | "
            f"{pull_requests_count} pull requests"
        )

    print("\nRaw data saved to:")
    print("data/raw_github_data.json")