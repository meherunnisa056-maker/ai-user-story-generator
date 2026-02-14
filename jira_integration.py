import os
import requests
from requests.auth import HTTPBasicAuth


def push_to_jira(summary, description):

    JIRA_URL = os.getenv("JIRA_URL")
    JIRA_EMAIL = os.getenv("JIRA_EMAIL")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

    if not JIRA_URL:
        print("JIRA_URL missing")
        return None
    if not JIRA_EMAIL:
        print("JIRA_EMAIL missing")
        return None
    if not JIRA_API_TOKEN:
        print("JIRA_API_TOKEN missing")
        return None
    if not JIRA_PROJECT_KEY:
        print("JIRA_PROJECT_KEY missing")
        return None

    url = f"{JIRA_URL}/rest/api/3/issue"

    # Jira Cloud requires ADF format
    description_adf = {
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
            "description": description_adf,
            "issuetype": {
                "name": "Task"
            }
        }
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
        )

        print("JIRA STATUS:", response.status_code)
        print("JIRA RESPONSE:", response.text)

        if response.status_code == 201:
            return response.json()["key"]

        return None

    except Exception as e:
        print("JIRA ERROR:", str(e))
        return None
