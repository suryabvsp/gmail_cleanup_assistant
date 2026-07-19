import time

from gmail_client import iterate_message_ids, get_message_metadata
from parser import parse_message
from database import (
    get_connection,
    load_existing_ids,
    insert_email,
)


COMMIT_EVERY = 100
PRINT_EVERY = 250


def format_eta(seconds):
    if seconds < 60:
        return f"{int(seconds)} sec"

    minutes = int(seconds // 60)

    if minutes < 60:
        return f"{minutes} min"

    hours = minutes // 60
    minutes %= 60

    return f"{hours}h {minutes}m"


def scan_mailbox(service, total_messages):

    conn = get_connection()

    existing_ids = load_existing_ids(conn)

    print(f"\nLoaded {len(existing_ids):,} existing emails.\n")

    processed = 0
    inserted = 0
    skipped = 0

    start_time = time.time()

    try:

        for message_id in iterate_message_ids(service):

            processed += 1

            if message_id in existing_ids:
                skipped += 1
                continue

            metadata = get_message_metadata(
                service,
                message_id,
            )

            parsed = parse_message(metadata)

            insert_email(conn, parsed)

            existing_ids.add(message_id)

            inserted += 1

            if inserted > 0 and inserted % COMMIT_EVERY == 0:
                conn.commit()

            if processed % PRINT_EVERY == 0:

                elapsed = time.time() - start_time

                speed = processed / elapsed if elapsed else 0

                remaining = max(0, total_messages - processed)

                eta = remaining / speed if speed else 0

                print(
                    f"Processed: {processed:,} | "
                    f"Inserted: {inserted:,} | "
                    f"Skipped: {skipped:,}"
                )

                print(
                    f"Speed: {speed:.2f} emails/sec | "
                    f"ETA: {format_eta(eta)}\n"
                )

        conn.commit()

    except KeyboardInterrupt:

        print("\nInterrupted. Saving progress...")

        conn.commit()

    finally:

        conn.close()

    elapsed = time.time() - start_time

    print("\n===== Scan Complete =====\n")

    print(f"Processed : {processed:,}")
    print(f"Inserted  : {inserted:,}")
    print(f"Skipped   : {skipped:,}")
    print(f"Elapsed   : {elapsed/60:.1f} minutes")