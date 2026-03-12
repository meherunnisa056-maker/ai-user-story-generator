# -------------------------------------------------
# ROLE AND ACTION DETECTION
# -------------------------------------------------

def detect_role_action(text):

    text = text.strip()

    if not text:
        return "User", "perform an action"

    words = text.split()

    roles = [
        "user","admin","customer","seller","buyer","student",
        "teacher","doctor","patient","employee","manager",
        "passenger","client","member","guest"
    ]

    first = words[0].lower()

    if first in roles and len(words) > 1:
        role = words[0]
        action = " ".join(words[1:])
        return role.capitalize(), action

    return "User", text


# -------------------------------------------------
# WHY GENERATOR
# -------------------------------------------------

def generate_smart_why(role, action):

    action = action.lower()

    if "search" in action:
        return "quickly locate the required information"

    if "order" in action:
        return "complete the purchasing process"

    if "payment" in action:
        return "complete the transaction securely"

    if "login" in action:
        return "securely access the system"

    if "register" in action:
        return "create and manage an account"

    if "upload" in action:
        return "store required information in the system"

    if "download" in action:
        return "retrieve stored information"

    if "update" in action:
        return "keep system data accurate"

    if "delete" in action:
        return "remove unnecessary data"

    if "book" in action:
        return "successfully reserve the required service"

    return "successfully perform the intended task"


# -------------------------------------------------
# EXPANDED USER STORY GENERATOR
# -------------------------------------------------

def generate_user_story(role, action, why):

    role = role.lower()
    action = action.lower()

    story = f"""
As a {role}, I want to {action} using the system so that I can {why}.
The system should provide an intuitive interface that allows the {role}
to perform this operation easily while ensuring the process is handled
efficiently and the necessary information is processed correctly.
"""

    return story.strip()


# -------------------------------------------------
# DESCRIPTION GENERATOR (SRS STYLE)
# -------------------------------------------------

def generate_description(role, action):

    role = role.lower()
    action = action.lower()

    description = f"""
The system shall allow the {role} to {action}.
The system must provide appropriate functionality to support this operation.
All inputs provided by the {role} must be validated before processing.
The system shall ensure that the requested operation is executed correctly.
Relevant data generated during the operation must be stored securely.
The system should provide confirmation or feedback to the user after completion.
"""

    return description.strip()


# -------------------------------------------------
# ACCEPTANCE CRITERIA GENERATOR
# -------------------------------------------------

def generate_acceptance_criteria(role, action):

    role = role.lower()
    action = action.lower()

    criteria = []

    criteria.append(f"The system shall allow the {role} to {action}.")
    criteria.append("The system shall validate all required inputs before processing.")
    criteria.append("The system shall securely store the generated data.")
    criteria.append("The system shall display confirmation after successful completion.")
    criteria.append("The system shall display appropriate error messages for invalid input.")

    if "login" in action:
        criteria.append("The system shall authenticate user credentials.")
        criteria.append("The system shall restrict access for invalid login attempts.")

    if "order" in action:
        criteria.append("The system shall verify product availability.")
        criteria.append("The system shall generate a unique order ID.")

    if "payment" in action:
        criteria.append("The system shall support secure payment processing.")
        criteria.append("The system shall generate a transaction confirmation.")

    if "upload" in action:
        criteria.append("The system shall allow uploading supported file formats.")
        criteria.append("The system shall store uploaded files securely.")

    if "book" in action:
        criteria.append("The system shall allow selection of available options.")
        criteria.append("The system shall confirm the reservation successfully.")

    return criteria


# -------------------------------------------------
# ARTICLE FIX
# -------------------------------------------------

def get_article(word):

    word = word.lower()

    if word.startswith(("a","e","i","o","u")):
        return "an"

    return "a"