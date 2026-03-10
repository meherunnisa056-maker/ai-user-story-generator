# -------------------------------------------------
# ROLE DETECTION
# -------------------------------------------------
def detect_role_action(text):

    text = text.strip()

    if not text:
        return "User", "perform action"

    words = text.split()

    invalid_roles = [
        "biometric", "authentication", "login", "logout",
        "payment", "checkout", "otp", "password",
        "face", "fingerprint", "system", "application"
    ]

    valid_roles = [
        "user", "admin", "customer", "buyer", "seller",
        "student", "teacher", "employee", "manager",
        "doctor", "patient", "passenger"
    ]

    first_word = words[0].lower()

    if first_word in valid_roles and len(words) > 1:
        role = words[0]
        action = " ".join(words[1:])
        return role.capitalize(), action

    if first_word in invalid_roles:
        return "User", text

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
        return "securely access the system"

    elif "register" in action:
        return "create a new account"

    elif "search" in action:
        return "find relevant information quickly"

    elif "add" in action:
        return "include selected items for further processing"

    elif "order" in action:
        return "complete the purchasing process"

    elif "payment" in action:
        return "complete the transaction securely"

    elif "upload" in action:
        return "store required files in the system"

    elif "download" in action:
        return "access stored files when needed"

    elif "update" in action:
        return "keep information accurate and updated"

    elif "delete" in action:
        return "remove unnecessary information"

    elif "manage" in action:
        return "control and maintain system data"

    elif "view" in action:
        return "access the required information"

    else:
        return "complete the required task efficiently"


# -------------------------------------------------
# SMART DESCRIPTION GENERATOR
# -------------------------------------------------
def generate_description(role, action):

    action = action.lower()

    if "login" in action:
        return f"This feature enables the {role.lower()} to log into the system using valid credentials. The system verifies the authentication details and grants secure access to the user dashboard."

    elif "register" in action:
        return f"This functionality allows the {role.lower()} to create a new account by providing the required personal and login details. The system validates the information and securely stores the account data."

    elif "search" in action:
        return f"This feature allows the {role.lower()} to search for specific items or information within the system using keywords or filters, helping the user quickly locate the required results."

    elif "add" in action and "cart" in action:
        return f"This functionality enables the {role.lower()} to add selected products to the shopping cart so that multiple items can be reviewed before proceeding with the purchase."

    elif "place order" in action or "order" in action:
        return f"This feature allows the {role.lower()} to confirm and place an order for selected products after reviewing the items in the cart and providing the required delivery information."

    elif "payment" in action:
        return f"This functionality enables the {role.lower()} to complete the payment process using secure payment methods supported by the system."

    elif "upload" in action:
        return f"This feature allows the {role.lower()} to upload documents, images, or files to the system so that they can be stored and accessed when needed."

    elif "download" in action:
        return f"This functionality enables the {role.lower()} to download stored files or documents from the system for offline access."

    elif "update" in action:
        return f"This feature allows the {role.lower()} to update existing information in the system, ensuring that the stored data remains accurate and up to date."

    elif "delete" in action:
        return f"This functionality enables the {role.lower()} to remove unwanted or outdated data from the system."

    elif "view" in action:
        return f"This feature allows the {role.lower()} to view the required information or records stored in the system."

    elif "manage" in action:
        return f"This functionality enables the {role.lower()} to manage system resources such as users, products, or records to ensure smooth system operation."

    else:
        return f"This feature enables the {role.lower()} to {action.lower()} within the system so that the required task can be completed efficiently."


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