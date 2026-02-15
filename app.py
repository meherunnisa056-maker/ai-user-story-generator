from flask import Flask, render_template, request, redirect, url_for
import os

# Optional OCR support
try:
    from PIL import Image
    import pytesseract
except:
    pytesseract = None

from ai_logic import detect_role_action, generate_smart_why, get_article
from jira_integration import push_to_jira

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

        role, action = detect_role_action(line)

        article = get_article(role)

        why = generate_smart_why(role, action)

        title = f"{role} – {action.capitalize()}"

        user_story = (
            f"As {article} {role.lower()}, "
            f"I want to {action.lower()} "
            f"so that I can {why.lower()}."
        )

        # Push to Jira
        jira_key = push_to_jira(title, user_story)

        status = (
            f"✅ Successfully pushed to Jira ({jira_key})"
            if jira_key else
            "⚠️ Jira push failed"
        )

        output += f"""
        <div class="story-card">

        <h3>Title</h3>
        <p><b>{title}</b></p>

        <h4>Who</h4>
        <p>{role} — The person who interacts with the system.</p>

        <h4>What</h4>
        <p>{action.capitalize()} — The functionality the user wants to perform.</p>

        <h4>Why</h4>
        <p>{why.capitalize()} — The benefit the user gets.</p>

        <h4>User Story</h4>
        <p>{user_story}</p>

        <h4>Acceptance Criteria</h4>
        <ul>
        <li>The system shall allow the {role.lower()} to {action.lower()}.</li>
        <li>The system shall validate inputs properly.</li>
        <li>The system shall display appropriate success or error messages.</li>
        <li>The system shall ensure data security and integrity.</li>
        <li>The feature shall work across supported devices and browsers.</li>
        </ul>

        <h4>Status</h4>
        <p>{status}</p>

        </div>
        """

    return output


# ---------------------------------------------------
# Home
# ---------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", output="")


# ---------------------------------------------------
# Generate
# ---------------------------------------------------
@app.route("/generate", methods=["POST"])
def generate():

    input_text = request.form.get("requirement", "").strip()

    # Voice input
    voice_text = request.form.get("voice_text", "").strip()

    if voice_text:
        input_text += "\n" + voice_text

    # Image OCR
    if "image" in request.files and pytesseract:

        image = request.files["image"]

        if image.filename:

            path = os.path.join(UPLOAD_FOLDER, image.filename)

            image.save(path)

            extracted = pytesseract.image_to_string(Image.open(path))

            input_text += "\n" + extracted

    if not input_text:

        return render_template(
            "index.html",
            output="<p style='color:red'>Please enter input</p>"
        )

    stories = generate_user_stories(input_text)

    return render_template("index.html", output=stories)


# ---------------------------------------------------
# Clear
# ---------------------------------------------------
@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("home"))


# ---------------------------------------------------
# Railway run
# ---------------------------------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
