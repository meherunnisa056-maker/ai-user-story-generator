def detect_role_action(text):
    text = text.strip()

    words = text.split()

    if len(words) < 2:
        return "User", text

    role = words[0]
    action = " ".join(words[1:])

    return role.capitalize(), action


# -------------------------------------------------
# SMART WHY GENERATOR
# -------------------------------------------------
def generate_smart_why(role, action):
    action_lower = action.lower()

    if "create" in action_lower:
        return "add new information to the system efficiently"
    elif "update" in action_lower or "edit" in action_lower:
        return "modify existing information accurately"
    elif "delete" in action_lower:
        return "remove unnecessary data securely"
    elif "view" in action_lower:
        return "access important information quickly"
    elif "login" in action_lower:
        return "securely access my account"
    elif "register" in action_lower:
        return "create an account and use the system"
    elif "upload" in action_lower:
        return "store files safely in the system"
    elif "download" in action_lower:
        return "retrieve files whenever needed"
    elif "pay" in action_lower or "checkout" in action_lower:
        return "complete my transaction securely"
    elif "search" in action_lower:
        return "find relevant information easily"
    else:
        return "complete my task efficiently"


# -------------------------------------------------
# ARTICLE FIX (a / an)
# -------------------------------------------------
def get_article(word):
    vowels = "aeiou"
    if word[0].lower() in vowels:
        return "an"
    return "a"
