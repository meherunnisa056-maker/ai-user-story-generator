import os
import requests
from requests.auth import HTTPBasicAuth

def push_to_jira(summary, description):

    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")
    jira_project = os.getenv("JIRA_PROJECT_KEY")

    print("DEBUG:")
    print("URL:", jira_url)
    print("EMAIL:", jira_email)
    print("PROJECT:", jira_project)

    if not jira_url or not jira_email or not jira_token or not jira_project:
        print("ERROR: Missing Jira variables")
        return None

    api_url = f"{jira_url}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {
                "key": jira_project
            },
            "summary": summary,
            "description": {
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
            },
            "issuetype": {
                "name": "Story"
            }
        }
    }

    response = requests.post(
        api_url,
        json=payload,
        auth=HTTPBasicAuth(jira_email, jira_token),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code == 201:
        return response.json()["key"]

    return None
