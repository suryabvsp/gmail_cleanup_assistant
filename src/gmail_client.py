from googleapiclient.discovery import build


def get_gmail_service(credentials):
    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


def get_profile(service):
    return service.users().getProfile(userId="me").execute()

def list_messages(service, max_results=500, page_token=None):
    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results,
            pageToken=page_token,
        )
        .execute()
    )

    return results

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

def iterate_message_ids(service):
    page_token = None

    while True:
        response = list_messages(
            service,
            max_results=500,
            page_token=page_token,
        )

        messages = response.get("messages", [])

        for message in messages:
            yield message["id"]

        page_token = response.get("nextPageToken")

        if not page_token:
            break