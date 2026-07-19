from gmail_client import (
    search_message_ids,
    get_message_metadata,
    trash_messages,
)
from database import search_sender

def preview_sender(service):

    sender = input("Sender email: ").strip()

    years = input("Older than how many years? ").strip()

    query = f"from:{sender} older_than:{years}y"

    print()
    print("Searching...")
    print(query)
    print()

    #rows = search_sender(sender)

    # message_ids = []

    # total_emails = len(rows)

    # total_size = 0

    # print()

    # for row in rows[:10]:
    #     print(row["subject"])

    # for row in rows:

    #     message_ids.append(row["message_id"])

    #     total_size += row["size_estimate"]

    message_ids = []

    total_emails = 0
    total_size = 0
    shown = 0

    for message_id in search_message_ids(service, query):

        message_ids.append(message_id)

        metadata = get_message_metadata(service, message_id)

        total_emails += 1
        total_size += metadata.get("sizeEstimate", 0)

        if shown < 10:

            subject = "(No Subject)"

            for header in metadata["payload"]["headers"]:

                if header["name"].lower() == "subject":
                    subject = header["value"]
                    break

            print(subject)

            shown += 1

    print()
    print("=" * 60)
    print(f"Matching emails : {total_emails:,}")
    print(
        f"Estimated size  : {total_size / (1024 * 1024):.2f} MB"
    )
    print("=" * 60)

    answer = input(
        "\nMove ALL matching emails to Trash? (yes/no): "
    ).strip().lower()

    if answer != "yes":
        print("\nCancelled.")
        return
    
    print("\nMoving emails to Trash...\n")

    BATCH_SIZE = 1000

    trashed = 0

    for i in range(0, len(message_ids), BATCH_SIZE):

        batch = message_ids[i:i + BATCH_SIZE]

        trash_messages(service, batch)

        trashed += len(batch)

        print(f"Moved {trashed:,} emails...")

    print(f"\nDone. Moved {trashed:,} emails to Trash.")