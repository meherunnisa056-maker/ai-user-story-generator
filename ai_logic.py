# -------------------------------------------------
# ROLE + ACTION DETECTION (Improved)
# -------------------------------------------------

def detect_role_action(text):

    text = text.strip()

    if not text:
        return "User", "perform an action"

    words = text.split()

    invalid_roles = [
        "biometric", "authentication", "login", "logout",
        "payment", "checkout", "otp", "password",
        "face", "fingerprint", "system", "application"
    ]

    valid_roles = [
        "user", "admin", "customer", "buyer", "seller",
        "student", "teacher", "employee", "manager"
    ]

    first_word = words[0].lower()

    # Case 1: Valid role detected
    if first_word in valid_roles and len(words) > 1:
        role = words[0].capitalize()
        action = " ".join(words[1:])
        return role, action

    # Case 2: Invalid role word → treat entire text as action
    if first_word in invalid_roles:
        return "User", text

    # Case 3: Multiple words but first not valid role
    if len(words) > 1:
        return "User", text

    # Case 4: Single word input → convert noun to action phrase
    return "User", f"access {text}"


# -------------------------------------------------
# SMART WHY GENERATOR
# -------------------------------------------------

def generate_smart_why(role, action):

    action = action.lower()

    if "login" in action:
        return "securely access my account"

    elif "register" in action or "signup" in action:
        return "create and manage my account"

    elif "logout" in action:
        return "securely exit the system"

    elif "upload" in action:
        return "store my files safely"

    elif "download" in action:
        return "access my files when needed"

    elif "delete" in action:
        return "remove unnecessary data securely"

    elif "update" in action or "edit" in action:
        return "modify information accurately"

    elif "create" in action:
        return "add new information to the system"

    elif "view" in action:
        return "access information easily"

    elif "search" in action:
        return "find information quickly"

    elif "payment" in action or "pay" in action:
        return "complete my transaction securely"

    elif "authentication" in action or "authenticate" in action:
        return "verify my identity securely"

    else:
        return "complete my task efficiently"


# -------------------------------------------------
# ARTICLE FIX (a / an)
# -------------------------------------------------

def get_article(word):

    word = word.lower()

    special_a = ["user", "university", "unique"]

    if word in special_a:
        return "a"

    vowels = ["a", "e", "i", "o", "u"]

    if word[0] in vowels:
        return "an"

    return "a"


# -------------------------------------------------
# USER STORY GENERATOR (MAIN FUNCTION)
# -------------------------------------------------

def generate_user_story(input_text):

    role, action = detect_role_action(input_text)

    why = generate_smart_why(role, action)

    article = get_article(role)

    title = f"{role} – {action.capitalize()}"

    user_story = f"As {article} {role.lower()}, I want to {action.lower()} so that I can {why}."

    acceptance_criteria = [
        f"The system shall allow the {role.lower()} to {action.lower()}.",
        "The system shall validate inputs properly.",
        "The system shall display appropriate success or error messages.",
        "The system shall ensure data security and integrity.",
        "The feature shall work across supported devices and browsers."
    ]

    return {
        "Title": title,
        "Role": role,
        "Action": action,
        "Why": why,
        "User Story": user_story,
        "Acceptance Criteria": acceptance_criteria
    }