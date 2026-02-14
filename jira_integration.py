import os
import requests
from requests.auth import HTTPBasicAuth


def push_to_jira(summary, description):

    JIRA_URL = os.getenv("JIRA_URL")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

    if not all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN, JIRA_PROJECT_KEY]):
        print("Missing Jira environment variables")
        return None

    url = f"{JIRA_URL}/rest/api/3/issue"

    # Jira Cloud requires ADF format for description
    adf_description = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": description
                    }
                ]
            }
        ]
    }

    payload = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": summary,
            "description": adf_description,
            "issuetype": {
                "name": "Task"
            }
        }
    }

    try:
        response = requests.post(
            url,
            json=payload,
            auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        print("Jira Status:", response.status_code)
        print("Jira Response:", response.text)

        if response.status_code == 201:
            return response.json()["key"]

        return None

    except Exception as e:
        print("Jira Error:", e)
        return None
