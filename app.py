from flask import Flask, render_template, request, redirect, url_for
import os

try:
    from PIL import Image
    import pytesseract
except:
    pytesseract = None

from ai_logic import (
    detect_role_action,
    generate_smart_why,
    generate_user_story,
    generate_description,
    generate_acceptance_criteria,
    get_article
)

from jira_integration import push_to_jira

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generate_user_stories(text):

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    output = ""

    for line in lines:

        role, action = detect_role_action(line)

        article = get_article(role)

        why = generate_smart_why(role, action)

        description = generate_description(role, action)

        story = generate_user_story(role, action, why)

        criteria = generate_acceptance_criteria(role, action)

        criteria_html = "".join([f"<li>{c}</li>" for c in criteria])

        title = f"{role} – {action.capitalize()}"

        jira_key = push_to_jira(title, story)

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
        <p>{role} — The person interacting with the system.</p>

        <h4>What</h4>
        <p>{action.capitalize()} — The functionality requested.</p>

        <h4>Why</h4>
        <p>{why.capitalize()}</p>

        <h4>Description</h4>
        <p>{description}</p>

        <h4>User Story</h4>
        <p>{story}</p>

        <h4>Acceptance Criteria</h4>
        <ul>
        {criteria_html}
        </ul>

        <h4>Status</h4>
        <p>{status}</p>

        </div>
        """

    return output


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", output="")


@app.route("/generate", methods=["POST"])
def generate():

    input_text = request.form.get("requirement", "").strip()

    voice_text = request.form.get("voice_text", "").strip()

    if voice_text:
        input_text += "\n" + voice_text

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


@app.route("/clear", methods=["POST"])
def clear():
    return redirect(url_for("home"))


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)