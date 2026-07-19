from auth import authenticate
from gmail_client import get_gmail_service, get_profile


def main():
    creds = authenticate()

    service = get_gmail_service(creds)

    profile = get_profile(service)

    print("\n===== Gmail Profile =====")
    print(f"Email Address : {profile['emailAddress']}")
    print(f"Total Messages: {profile['messagesTotal']:,}")
    print(f"Total Threads : {profile['threadsTotal']:,}")


if __name__ == "__main__":
    main()