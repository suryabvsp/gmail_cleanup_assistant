from database import get_connection
import re

def top_senders(limit=50):
    conn = get_connection()

    rows = conn.execute("""
    SELECT
        sender,
        size_estimate
    FROM emails
    """).fetchall()

    conn.close()

    grouped = {}

    for row in rows:

        email = extract_email(row["sender"])

        if email not in grouped:
            grouped[email] = {
                "email": email,
                "email_count": 0,
                "total_size": 0,
            }

        grouped[email]["email_count"] += 1
        grouped[email]["total_size"] += row["size_estimate"]

    results = sorted(
        grouped.values(),
        key=lambda x: x["total_size"],
        reverse=True,
    )

    for row in results[:limit]:

        size_mb = row["total_size"] / (1024 * 1024)

        print(
            f"{row['email_count']:>8} "
            f"{size_mb:>10.1f} "
            f"{row['email']}"
        )

def extract_email(sender):
    match = re.search(r"<([^>]+)>", sender)

    if match:
        return match.group(1).lower()

    return sender.strip().lower()