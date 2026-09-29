DROP TABLE IF EXISTS repo_health_summary;

CREATE TABLE repo_health_summary AS

WITH issue_metrics AS (
    SELECT
        repository_id,
        COUNT(*) AS total_issues,
        SUM(CASE WHEN state = 'open' THEN 1 ELSE 0 END) AS open_issues,
        SUM(CASE WHEN state = 'closed' THEN 1 ELSE 0 END) AS closed_issues
    FROM issues
    GROUP BY repository_id
),

pull_request_metrics AS (
    SELECT
        repository_id,
        COUNT(*) AS total_pull_requests,
        SUM(CASE WHEN state = 'open' THEN 1 ELSE 0 END) AS open_pull_requests,
        SUM(CASE WHEN state = 'closed' THEN 1 ELSE 0 END) AS closed_pull_requests,
        SUM(CASE WHEN merged_at IS NOT NULL THEN 1 ELSE 0 END) AS merged_pull_requests
    FROM pull_requests
    GROUP BY repository_id
)

SELECT
    r.repository_id,
    r.full_name,
    r.stars,
    r.forks,
    r.open_issues,

    COALESCE(i.total_issues, 0) AS total_issues,
    COALESCE(i.open_issues, 0) AS tracked_open_issues,
    COALESCE(i.closed_issues, 0) AS closed_issues,

    COALESCE(p.total_pull_requests, 0) AS total_pull_requests,
    COALESCE(p.open_pull_requests, 0) AS open_pull_requests,
    COALESCE(p.closed_pull_requests, 0) AS closed_pull_requests,
    COALESCE(p.merged_pull_requests, 0) AS merged_pull_requests,

    CASE
        WHEN COALESCE(i.total_issues, 0) > 0
        THEN ROUND(
            CAST(i.closed_issues AS REAL) / i.total_issues * 100,
            2
        )
        ELSE 0
    END AS issue_closure_rate,

    CASE
        WHEN COALESCE(p.total_pull_requests, 0) > 0
        THEN ROUND(
            CAST(p.merged_pull_requests AS REAL)
            / p.total_pull_requests * 100,
            2
        )
        ELSE 0
    END AS pull_request_merge_rate

FROM repositories r

LEFT JOIN issue_metrics i
    ON r.repository_id = i.repository_id

LEFT JOIN pull_request_metrics p
    ON r.repository_id = p.repository_id;