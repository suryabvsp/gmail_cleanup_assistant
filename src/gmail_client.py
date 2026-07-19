from googleapiclient.discovery import build


def get_gmail_service(credentials):
    return build(
        "gmail",
        "v1",
        credentials=credentials
    )


def get_profile(service):
    return service.users().getProfile(userId="me").execute()