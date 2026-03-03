def push_to_jira(summary, description):

    jira_url = os.getenv("JIRA_URL")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_token = os.getenv("JIRA_API_TOKEN")
    jira_project = os.getenv("JIRA_PROJECT_KEY")

    if not jira_url or not jira_email or not jira_token or not jira_project:
        print("ERROR: Missing Jira variables")
        return None

    api_url = jira_url.rstrip("/") + "/rest/api/3/issue"

    summary = summary[:250] if summary else "AI Generated Story"

    payload = {
        "fields": {
            "project": {"key": jira_project},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": description}
                        ]
                    }
                ]
            },
            "issuetype": {"name": "Task"}  # changed here
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