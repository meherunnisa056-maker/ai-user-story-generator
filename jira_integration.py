import os
import requests
from requests.auth import HTTPBasicAuth

def push_to_jira(summary, description):

    url = os.getenv("JIRA_URL")
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")
    project = os.getenv("JIRA_PROJECT_KEY")

    if not url or not email or not token or not project:
        print("Jira variables missing")
        return None

    api = f"{url}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {"key": project},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Story"}
        }
    }

    response = requests.post(
        api,
        json=payload,
        auth=HTTPBasicAuth(email, token),
        headers={"Content-Type": "application/json"}
    )

    print(response.status_code, response.text)

    if response.status_code == 201:
        return response.json()["key"]

    return None
