from email.utils import parseaddr


def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def extract_domain(sender):
    _, email = parseaddr(sender)

    if "@" not in email:
        return ""

    return email.split("@")[-1].lower()


def has_attachment(payload):
    if payload.get("filename"):
        return True

    for part in payload.get("parts", []):
        if has_attachment(part):
            return True

    return False


def get_category(labels):
    for label in labels:
        if label.startswith("CATEGORY_"):
            return label

    return ""


def parse_message(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = get_header(headers, "From")

    return {
        "message_id": message.get("id", ""),
        "thread_id": message.get("threadId", ""),
        "sender": sender,
        "sender_domain": extract_domain(sender),
        "subject": get_header(headers, "Subject"),
        "date": get_header(headers, "Date"),
        "size_estimate": message.get("sizeEstimate", 0),
        "has_attachment": has_attachment(payload),
        "labels": ",".join(message.get("labelIds", [])),
        "category": get_category(message.get("labelIds", [])),
    }