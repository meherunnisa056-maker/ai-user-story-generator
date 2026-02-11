from flask import Flask, render_template, request, redirect, url_for
import os
import base64
import requests
from PIL import Image
import pytesseract
from dotenv import load_dotenv
from ai_logic import detect_role_action

# Load environment variables
load_dotenv()

app = Flask(__name__)

# 🔹 Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\SHAIK YOUSUF\Documents\5A6\tesseract.exe"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -------------------------------------------------
# 🔹 JIRA AUTOMATIC PUSH FUNCTION (STEP-1 FIX)
# -------------------------------------------------
def push_to_jira(summary, description):
    jira_domain = os.getenv("JIRA_DOMAIN")
    jira_email = os.getenv("JIRA_EMAIL")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    project_key = os.getenv("JIRA_PROJECT_KEY")

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
            "issuetype": {"name": "Story"},   # ✅ FIXED (Task → Story)
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

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return response.json()["key"]
    else:
        print("❌ Jira Error:", response.status_code, response.text)
        return None

# -------------------------------------------------
# 🔹 ROUTES
# -------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    input_text = request.form.get("requirement", "").strip()
    extracted_text = ""

    # 🎤 Voice input
    voice_text = request.form.get("voice_text", "").strip()
    if voice_text:
        input_text += "\n" + voice_text

    # 🖼 Image OCR
    if "image" in request.files:
        image = request.files["image"]
        if image.filename:
            path = os.path.join(UPLOAD_FOLDER, image.filename)
            image.save(path)
            extracted_text = pytesseract.image_to_string(Image.open(path))
            input_text += "\n" + extracted_text

    if not input_text.strip():
        return render_template(
            "index.html",
            output="<p style='color:red'>❌ Please enter text, voice, or image</p>"
        )

    stories_html = generate_user_stories(input_text)

    return render_template(
        "index.html",
        output=stories_html
    )

@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("home"))

# -------------------------------------------------
# 🔹 USER STORY GENERATION + JIRA PUSH
# -------------------------------------------------
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
            "❌ Jira push failed"
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

if __name__ == "__main__":
    app.run(debug=True)
