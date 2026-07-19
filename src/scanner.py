from gmail_client import iterate_message_ids, get_message_metadata
from parser import parse_message
from database import insert_email, email_exists


def scan_mailbox(service):
    processed = 0
    inserted = 0
    skipped = 0

    print("\nScanning mailbox...\n")

    for message_id in iterate_message_ids(service):

        processed += 1

        if email_exists(message_id):
            skipped += 1
            continue

        metadata = get_message_metadata(service, message_id)

        parsed = parse_message(metadata)

        insert_email(parsed)

        inserted += 1

        if processed % 25 == 0:
            print(
                f"Processed: {processed:,} | "
                f"Inserted: {inserted:,} | "
                f"Skipped: {skipped:,}"
            )

    print("\nScan complete.\n")

    print(f"Processed : {processed:,}")
    print(f"Inserted  : {inserted:,}")
    print(f"Skipped   : {skipped:,}")