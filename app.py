from flask import Flask, render_template, request, redirect, url_for
import os
import base64
import requests
from dotenv import load_dotenv
from ai_logic import detect_role_action

# ---------------------------------------
# Load environment variables
# ---------------------------------------
load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------------
# JIRA PUSH FUNCTION
# ---------------------------------------
def push_to_jira(summary, description):
    jira_domain = os.getenv("JIRA_DOMAIN")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    project_key = os.getenv("JIRA_PROJECT_KEY")

    # If any env variable missing, skip Jira
    if not all([jira_domain, jira_email, jira_api_token, project_key]):
        print("❌ Missing Jira environment variables")
        return None

    url = f"https://{jira_domain}/rest/api/3/issue"

    auth_string = f"{jira_email}:{jira_api_token}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": "Story"},
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
            }
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            return response.json().get("key")
        else:
            print("❌ Jira Error:", response.status_code, response.text)
            return None

    except Exception as e:
        print("❌ Jira Exception:", e)
        return None


# ---------------------------------------
# ROUTES
# ---------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    input_text = request.form.get("requirement", "").strip()

    # Voice input
    voice_text = request.form.get("voice_text", "").strip()
    if voice_text:
        input_text += "\n" + voice_text

    if not input_text:
        return render_template(
            "index.html",
            output="<p style='color:red'>❌ Please enter some requirement text</p>"
        )

    stories_html = generate_user_stories(input_text)

    return render_template("index.html", output=stories_html)


@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("home"))


# ---------------------------------------
# USER STORY GENERATION
# ---------------------------------------
def generate_user_stories(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    output = ""

    for line in lines:
        role, action = detect_role_action(line)

        user_story = (
            f"As a {role.lower()}, I want to {action} "
            f"so that I can achieve my objective."
        )

        jira_key = push_to_jira(
            summary=f"{role} – {action.capitalize()}",
            description=user_story
        )

        status = (
            f"✅ Pushed to Jira successfully (Issue: {jira_key})"
            if jira_key else
            "⚠️ Jira not configured or push failed"
        )

        output += f"""
        <div class="story-card">
            <h3>Title</h3>
            <p><b>{role} – {action.capitalize()}</b></p>

            <h4>User Story</h4>
            <p>{user_story}</p>

            <h4>Acceptance Criteria</h4>
            <ul>
                <li>The system shall allow the {role.lower()} to {action}.</li>
                <li>Inputs shall be validated correctly.</li>
                <li>Success and error messages shall be displayed.</li>
                <li>The feature shall work across supported devices.</li>
            </ul>

            <h4>Status</h4>
            <p>{status}</p>
        </div>
        """

    return output


# ---------------------------------------
# PRODUCTION RUN (Railway)
# ---------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
