from src.gmail_service import get_gmail_service
from src.email_parser import extract_email_data
from src.sheets_service import get_sheets_service, append_row
from src.state_manager import load_state, save_state


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    processed_ids = load_state()

    results = gmail_service.users().messages().list(
        userId="me",
        labelIds=["INBOX", "UNREAD"]
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("No unread emails found.")
        return

    for msg in messages:
        msg_id = msg["id"]

        if msg_id in processed_ids:
            continue

        email = extract_email_data(gmail_service, msg_id)

        MAX_CONTENT_LENGTH = 10000

        safe_content = email["content"][:MAX_CONTENT_LENGTH]

        row = [
            email["from"],
            email["subject"],
            email["date"],
            safe_content
        ]   
        append_row(sheets_service, row)

        # Mark email as read
        gmail_service.users().messages().modify(
            userId="me",
            id=msg_id,
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

        processed_ids.add(msg_id)
        print("Processed:", email["subject"])

    save_state(processed_ids)


if __name__ == "__main__":
    main()
