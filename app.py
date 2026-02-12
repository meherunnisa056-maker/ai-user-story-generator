from flask import Flask, render_template, request
from ai_logic import detect_role_action, generate_smart_why, get_article
from jira_integration import push_to_jira

# IMPORTANT: This variable name must be "app"
app = Flask(__name__)


def generate_user_stories(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    output = ""

    for line in lines:
        role, action = detect_role_action(line)

        article = get_article(role)
        why = generate_smart_why(role, action)

        user_story = (
            f"As {article} {role.lower()}, "
            f"I want to {action.lower()} "
            f"so that I can {why}."
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
                <li>The feature shall follow security best practices.</li>
                <li>The feature shall work across supported devices and browsers.</li>
            </ul>

            <h4>Status</h4>
            <p>{status}</p>
        </div>
        """

    return output


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        if user_input.strip():
            result = generate_user_stories(user_input)

    return render_template("index.html", result=result)


# Required for local run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
