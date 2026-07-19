from auth import authenticate
from gmail_client import (
    get_gmail_service,
    get_profile,
    list_messages,
    get_message_metadata,
)
from database import initialize_database
from parser import parse_message
from database import initialize_database, insert_email

def main():
    initialize_database()
    creds = authenticate()

    service = get_gmail_service(creds)

    profile = get_profile(service)

    print("\n===== Gmail Profile =====")
    print(f"Email Address : {profile['emailAddress']}")
    print(f"Total Messages: {profile['messagesTotal']:,}")
    print(f"Total Threads : {profile['threadsTotal']:,}")

    messages = list_messages(service)

    print(f"\nRetrieved {len(messages)} message IDs")

    print("\nFirst five message IDs:")

    for message in messages[:5]:
        print(message["id"])

    first_id = messages[0]["id"]

    metadata = get_message_metadata(service, first_id)

    print("\n===== First Email Metadata =====")
    parsed = parse_message(metadata)
    print("\n===== Parsed Email =====")
    for key, value in parsed.items():
        print(f"{key:16}: {value}")

    insert_email(parsed)
    print("\nEmail successfully written to SQLite.")
    


if __name__ == "__main__":
    main()