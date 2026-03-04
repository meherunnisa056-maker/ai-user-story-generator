from flask import Flask, render_template, request, redirect, url_for
import os

# OCR imports
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


# -------------------------------------------------
# USER STORY GENERATION
# -------------------------------------------------
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

        <h4>User Story</h4>
        <p>{user_story}</p>

        <h4>Status</h4>
        <p>{status}</p>
        </div>
        """

    return output


# -------------------------------------------------
# HOME ROUTE
# -------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", output="", input_text="")


# -------------------------------------------------
# GENERATE ROUTE (VOICE + IMAGE + TEXT FIXED)
# -------------------------------------------------
@app.route("/generate", methods=["POST"])
def generate():

    typed_text = request.form.get("requirement", "").strip()
    voice_text = request.form.get("voice_text", "").strip()
    image = request.files.get("image")

    input_text = ""

    # Priority: Voice > Image > Typed
    if voice_text:
        input_text = voice_text

    elif image and image.filename and pytesseract:
        path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(path)

        try:
            extracted = pytesseract.image_to_string(Image.open(path)).strip()
            print("Extracted OCR:", extracted)
            input_text = extracted
        except:
            input_text = ""

    else:
        input_text = typed_text

    print("Final Input Sent To AI:", input_text)

    if not input_text:
        return render_template(
            "index.html",
            output="<p style='color:red'>Please enter input</p>",
            input_text=""
        )

    stories = generate_user_stories(input_text)

    return render_template(
        "index.html",
        output=stories,
        input_text=input_text
    )


# -------------------------------------------------
# CLEAR ROUTE
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