import requests
from requests.auth import HTTPBasicAuth

def fetch_sonar_issues(url: str, token: str, project_key: str):

    response = requests.get(
        f"{url}/api/issues/search",
        params={
            "componentKeys": project_key,
            "ps": 100
        },
        auth=HTTPBasicAuth(token, "")
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Sonar API error {response.status_code}: {response.text}"
        )

    return response.json().get("issues", [])


def sonar_summary(issues: list):

    severities = ["BLOCKER", "CRITICAL", "MAJOR", "MINOR", "INFO"]
    severity_count = {sev: 0 for sev in severities}

    for issue in issues:
        sev = issue.get("severity", "INFO")
        if sev in severity_count:
            severity_count[sev] += 1
        else:
            severity_count["INFO"] += 1

    total_issues = len(issues)
    status = "OK" if total_issues == 0 else "ISSUES FOUND"

    return severity_count, status
