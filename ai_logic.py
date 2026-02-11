def detect_role_action(sentence):
    sentence = sentence.lower()

    roles = ["admin", "user", "student", "teacher", "manager"]
    role = "User"

    for r in roles:
        if r in sentence:
            role = r.capitalize()
            sentence = sentence.replace(r, "").strip()
            break

    action = (
        sentence.replace("can", "")
        .replace("to", "")
        .replace("the", "")
        .strip()
    )

    return role, action
