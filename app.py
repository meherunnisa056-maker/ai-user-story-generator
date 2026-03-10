from flask import Flask, render_template, request, redirect, url_for
import os

# OCR imports
try:
    from PIL import Image
    import pytesseract
except:
    pytesseract = None

# AI logic imports
from ai_logic import (
    detect_role_action,
    get_article,
    generate_description,
    generate_user_story,
    generate_functional_requirements,
    generate_acceptance_criteria
)

# Jira integration
from jira_integration import push_to_jira

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -------------------------------------------------
# GENERATE USER STORIES
# -------------------------------------------------

def generate_user_stories(text):

    lines = [l.strip() for l in text.splitlines() if l.strip()]

    output = ""

    for line in lines:

        role, action = detect_role_action(line)

        article = get_article(role)

        description = generate_description(role, action)

        story = generate_user_story(role, action)

        functional_reqs = generate_functional_requirements(role, action)

        acceptance_criteria = generate_acceptance_criteria(role, action)

        title = f"{role} – {action.capitalize()}"

        # Push to Jira
        jira_key = push_to_jira(title, story)

        status = (
            f"✅ Successfully pushed to Jira ({jira_key})"
            if jira_key else
            "⚠️ Jira push failed"
        )

        # Convert lists to HTML
        functional_html = ""
        for req in functional_reqs:
            functional_html += f"<li>{req}</li>"

        acceptance_html = ""
        for ac in acceptance_criteria:
            acceptance_html += f"<li>{ac}</li>"

        output += f"""
        <div class="story-card">

        <h3>Title</h3>
        <p><b>{title}</b></p>

        <h4>Actor</h4>
        <p>{role}</p>

        <h4>Description</h4>
        <p>{description}</p>

        <h4>User Story</h4>
        <p>{story}</p>

        <h4>Functional Requirements</h4>
        <ul>
        {functional_html}
        </ul>

        <h4>Acceptance Criteria</h4>
        <ul>
        {acceptance_html}
        </ul>

        <h4>Status</h4>
        <p>{status}</p>

        </div>
        """

    return output


# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", output="")


# -------------------------------------------------
# GENERATE STORIES
# -------------------------------------------------

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

            extracted_text = pytesseract.image_to_string(Image.open(path))

            input_text += "\n" + extracted_text

    if not input_text:

        return render_template(
            "index.html",
            output="<p style='color:red'>Please enter input</p>"
        )

    stories = generate_user_stories(input_text)

    return render_template("index.html", output=stories)


# -------------------------------------------------
# CLEAR OUTPUT
# -------------------------------------------------

@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("home"))


# -------------------------------------------------
# RUN APP
# -------------------------------------------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)