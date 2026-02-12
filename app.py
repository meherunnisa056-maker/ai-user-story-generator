from flask import Flask, request, render_template_string

app = Flask(__name__)

# Home route (IMPORTANT - fixes Not Found error)
@app.route("/")
def home():
    return """
    <h2>AI User Story Generator</h2>
    <form method="POST" action="/generate">
        <textarea name="text" rows="6" cols="60"
        placeholder="Enter requirement here..."></textarea><br><br>
        <button type="submit">Generate User Stories</button>
    </form>
    """

@app.route("/generate", methods=["POST"])
def generate():
    text = request.form.get("text")
    if not text:
        return "No input provided."

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    output = ""

    for line in lines:
        role = "User"
        action = line

        user_story = f"As a {role}, I want to {action.lower()} so that I can achieve my goal."

        output += f"""
        <div style="border:1px solid #ccc;padding:15px;margin:10px;">
            <h3>{role} – {action.capitalize()}</h3>
            <p><b>User Story:</b> {user_story}</p>
            <ul>
                <li>The system shall allow the user to {action.lower()}.</li>
                <li>The system shall validate inputs before processing.</li>
                <li>The system shall show success or failure messages.</li>
            </ul>
        </div>
        """

    return f"""
    <h2>Generated User Stories</h2>
    {output}
    <br><a href="/">⬅ Back</a>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)