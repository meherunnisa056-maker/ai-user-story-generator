# -------------------------------------------------
# ROLE AND ACTION DETECTION
# -------------------------------------------------

def detect_role_action(text):

    text = text.strip()

    if not text:
        return "User", "perform an action"

    words = text.split()

    valid_roles = [
        "user", "admin", "customer", "buyer", "seller",
        "student", "teacher", "employee", "manager",
        "doctor", "patient", "passenger", "driver"
    ]

    first_word = words[0].lower()

    if first_word in valid_roles and len(words) > 1:
        role = words[0].capitalize()
        action = " ".join(words[1:])
    else:
        role = "User"
        action = text

    return role, action


# -------------------------------------------------
# ARTICLE FIX (a / an)
# -------------------------------------------------

def get_article(word):

    word = word.lower()

    special_a = ["user", "university", "unique"]

    if word in special_a:
        return "a"

    if word[0] in ["a", "e", "i", "o", "u"]:
        return "an"

    return "a"


# -------------------------------------------------
# DESCRIPTION GENERATOR
# -------------------------------------------------

def generate_description(role, action):

    return (
        f"The system allows the {role.lower()} to {action.lower()} "
        f"through the application interface while ensuring proper "
        f"validation, security, and successful completion of the requested operation."
    )


# -------------------------------------------------
# DETAILED USER STORY GENERATOR
# -------------------------------------------------

def generate_user_story(role, action):

    return (
        f"As a {role.lower()}, I want to {action.lower()} using the system "
        f"so that I can successfully accomplish the intended task in an efficient "
        f"and secure manner without facing operational difficulties."
    )


# -------------------------------------------------
# FUNCTIONAL REQUIREMENTS GENERATOR
# -------------------------------------------------

def generate_functional_requirements(role, action):

    return [
        f"The system shall allow the {role.lower()} to {action.lower()}.",
        "The system shall provide a user interface for performing the requested operation.",
        "The system shall validate the input data before processing the request.",
        "The system shall process the request according to system rules.",
        "The system shall display appropriate success or error messages.",
        "The system shall securely store or update the related data in the system database."
    ]


# -------------------------------------------------
# ACCEPTANCE CRITERIA GENERATOR
# -------------------------------------------------

def generate_acceptance_criteria(role, action):

    return [
        f"The {role.lower()} should be able to {action.lower()} successfully with valid inputs.",
        "The system should validate user inputs before processing.",
        "Invalid inputs should display appropriate error messages.",
        "The system should maintain data integrity and security during the operation.",
        "The feature should work correctly across supported devices and browsers."
    ]