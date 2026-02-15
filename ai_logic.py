# -------------------------------------------------
# ROLE DETECTION
# -------------------------------------------------
def detect_role_action(text):

    text = text.strip()

    if not text:
        return "User", "perform action"

    words = text.split()

    # Words that are NOT roles
    invalid_roles = [
        "biometric", "authentication", "login", "logout",
        "payment", "checkout", "otp", "password",
        "face", "fingerprint", "system", "application"
    ]

    # Valid roles
    valid_roles = [
        "user", "admin", "customer", "buyer", "seller",
        "student", "teacher", "employee", "manager"
    ]

    first_word = words[0].lower()

    # If first word is a valid role → use it
    if first_word in valid_roles and len(words) > 1:

        role = words[0]
        action = " ".join(words[1:])

        return role.capitalize(), action

    # If first word is invalid role → default to User
    if first_word in invalid_roles:

        return "User", text

    # Default logic
    if len(words) > 1:

        role = words[0]
        action = " ".join(words[1:])

        return role.capitalize(), action

    return "User", text


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

    # Special cases
    special_a = ["user", "university", "unique"]

    if word in special_a:
        return "a"

    vowels = ["a", "e", "i", "o", "u"]

    if word[0] in vowels:
        return "an"

    return "a"
