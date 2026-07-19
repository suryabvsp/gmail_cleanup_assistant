from auth import authenticate
from gmail_client import (
    get_gmail_service,
    get_profile,
)
from database import initialize_database
from parser import parse_message
from database import initialize_database, insert_email, get_email_count
from scanner import scan_mailbox
from analytics import top_senders

def main():
    initialize_database()
    creds = authenticate()

    service = get_gmail_service(creds)

    profile = get_profile(service)

    print("\n===== Gmail Profile =====")
    print(f"Email Address : {profile['emailAddress']}")
    print(f"Total Messages: {profile['messagesTotal']:,}")
    print(f"Total Threads : {profile['threadsTotal']:,}")

    # scan_mailbox(
    #     service,
    #     profile["messagesTotal"],
    # )

    top_senders()


if __name__ == "__main__":
    main()