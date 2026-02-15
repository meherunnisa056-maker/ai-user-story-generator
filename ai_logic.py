def detect_role_action(text):

    text = text.strip()

    words = text.split()

    if len(words) < 2:
        return "User", text

    role = words[0]
    action = " ".join(words[1:])

    return role.capitalize(), action


def generate_smart_why(role, action):

    action = action.lower()

    if "login" in action:
        return "securely access my account"

    if "register" in action:
        return "create and manage my account"

    if "buy" in action or "purchase" in action:
        return "complete my purchase easily"

    if "upload" in action:
        return "store my files safely"

    if "authentication" in action or "authenticate" in action:
        return "verify my identity securely"

    return "complete my task efficiently"


def get_article(word):

    if word[0].lower() in "aeiou":
        return "an"

    return "a"
