# ROLE AND ACTION DETECTION
def detect_role_action(text):
    text = text.strip()
    if not text:
        return "User", "perform an action"
    words = text.split()
    roles = [
        "user","admin","customer","seller","buyer","student",
        "teacher","doctor","patient","employee","manager",
        "passenger","client","member"
    ]
    first = words[0].lower()
    if first in roles and len(words) > 1:
        role = words[0]
        action = " ".join(words[1:])
        return role.capitalize(), action
    return "User", text
# WHY GENERATOR
def generate_smart_why(role, action):
    action = action.lower()
    if "search" in action:
        return "find the required information quickly"
    elif "order" in action:
        return "purchase the selected items successfully"
    elif "payment" in action:
        return "complete the transaction securely"
    elif "login" in action:
        return "securely access the system"
    elif "register" in action:
        return "create and manage an account"
    elif "upload" in action:
        return "store required files in the system"
    elif "download" in action:
        return "access files when needed"
    elif "update" in action:
        return "keep the information accurate"
    elif "delete" in action:
        return "remove unnecessary data"
    elif "book" in action:
        return "secure a reservation successfully"
    else:
        return "achieve the intended functionality of the system"
# DESCRIPTION GENERATOR 
def generate_description(role, action):
    role = role.lower()
    action = action.lower()
    description = f"""
The system shall allow the {role} to {action}.
The functionality should provide an interface that enables the {role} to perform the requested operation efficiently.
The system must validate all necessary inputs before executing the action.
All relevant information related to this operation shall be stored securely in the system database.
The system should ensure proper processing, confirmation, and reliability of the operation.
"""
    return description.strip()
# ACCEPTANCE CRITERIA GENERATOR
def generate_acceptance_criteria(role, action):
    role = role.lower()
    action = action.lower()
    criteria = []
    criteria.append(f"The system shall allow the {role} to {action}.")
    criteria.append("The system shall validate all required inputs before processing.")
    criteria.append("The system shall store the relevant data securely.")
    criteria.append("The system shall display confirmation after successful completion.")
    criteria.append("The system shall handle invalid inputs with appropriate error messages.")
    if "order" in action:
        criteria.append("The system shall verify product availability before confirming the order.")
        criteria.append("The system shall generate a unique order identifier.")
    if "login" in action:
        criteria.append("The system shall authenticate user credentials securely.")
        criteria.append("The system shall restrict access for invalid login attempts.")
    if "upload" in action:
        criteria.append("The system shall allow uploading supported file formats.")
        criteria.append("The system shall store uploaded files securely.")
    if "payment" in action:
        criteria.append("The system shall process payments using secure payment methods.")
        criteria.append("The system shall generate a payment confirmation.")
    if "book" in action:
        criteria.append("The system shall allow users to select available options.")
        criteria.append("The system shall confirm the reservation successfully.")
    return criteria
# ARTICLE FIX
def get_article(word):
    word = word.lower()
    if word.startswith(("a","e","i","o","u")):
        return "an"
    return "a"