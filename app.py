from flask import Flask, render_template, request, redirect, url_for
import os

# Optional imports (safe for Railway)
try:
    from PIL import Image
    import pytesseract
except:
    pytesseract = None

# AI logic import
from ai_logic import detect_role_action, generate_smart_why, get_article

# Safe Jira import (prevents Railway crash)
try:
    from jira_integration import push_to_jira
except:
    def push_to_jira(summary, description):
        return None


# ---------------------------------------------------
# Flask App
# ---------------------------------------------------
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------------------------------------------
# Generate User Stories
# ---------------------------------------------------
def generate_user_stories(text):

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    output = ""

    for line in lines:

        try:
            role, action = detect_role_action(line)
        except:
            role, action = "User", line

        article = get_article(role)

        try:
            why = generate_smart_why(role, action)
        except:
            why = "achieve my goal efficiently"

        user_story = (
            f"As {article} {role.lower()}, "
            f"I want to {action.lower()} "
            f"so that I can {why}."
        )

        # Safe Jira push
        jira_key = None
        try:
            jira_key = push_to_jira(
                summary=f"{role} – {action.capitalize()}",
                description=user_story
            )
        except:
            jira_key = None

        status = (
            f"✅ Pushed to Jira successfully (Issue: {jira_key})"
            if jira_key else
            "⚠️ Jira not configured or push failed"
        )

        output += f"""
        <div class="story-card">

            <h3>Title</h3>
            <p><b>{role} – {action.capitalize()}</b></p>

            <h4>Who</h4>
            <p>{role}</p>

            <h4>What</h4>
            <p>{action.capitalize()}</p>

            <h4>Why</h4>
            <p>{why.capitalize()}</p>

            <h4>User Story</h4>
            <p>{user_story}</p>

            <h4>Acceptance Criteria</h4>
            <ul>
                <li>The system shall allow the {role.lower()} to {action.lower()}.</li>
                <li>The system shall validate inputs before processing.</li>
                <li>The system shall display success or failure messages.</li>
                <li>The system shall follow security best practices.</li>
                <li>The feature shall work across devices and browsers.</li>
            </ul>

            <h4>Status</h4>
            <p>{status}</p>

        </div>
        """

    return output


# ---------------------------------------------------
# Home Route
# ---------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", output="")


# ---------------------------------------------------
# Generate Route
# ---------------------------------------------------
@app.route("/generate", methods=["POST"])
def generate():

    input_text = request.form.get("requirement", "").strip()

    # Voice input
    voice_text = request.form.get("voice_text", "").strip()

    if voice_text:
        input_text += "\n" + voice_text


    # Image input (safe OCR)
    if "image" in request.files:

        image = request.files["image"]

        if image.filename != "" and pytesseract is not None:

            try:
                path = os.path.join(UPLOAD_FOLDER, image.filename)
                image.save(path)

                extracted_text = pytesseract.image_to_string(
                    Image.open(path)
                )

                input_text += "\n" + extracted_text

            except:
                pass


    if not input_text.strip():

        return render_template(
            "index.html",
            output="<p style='color:red;'>Please enter text, voice, or image.</p>"
        )


    stories = generate_user_stories(input_text)

    return render_template(
        "index.html",
        output=stories
    )


# ---------------------------------------------------
# Clear Route
# ---------------------------------------------------
@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("home"))


# ---------------------------------------------------
# Railway / Production Run
# ---------------------------------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
