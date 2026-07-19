from googleapiclient.discovery import build


def get_gmail_service(credentials):
    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


def get_profile(service):
    return service.users().getProfile(userId="me").execute()

def list_messages(service, max_results=100):
    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results
        )
        .execute()
    )

    return results.get("messages", [])

def get_message_metadata(service, message_id):
    return (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"],
        )
        .execute()
    )