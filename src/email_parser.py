import base64
from email import message_from_bytes
from email.header import decode_header


def extract_email_data(service, message_id):
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="raw"
    ).execute()

    raw_email = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
    email_message = message_from_bytes(raw_email)

    sender = email_message.get("From", "")
    date = email_message.get("Date", "")

    # ---- FIX: Decode encoded subject properly ----
    raw_subject = email_message.get("Subject", "")
    decoded_subject_parts = decode_header(raw_subject)

    subject = ""
    for part, encoding in decoded_subject_parts:
        if isinstance(part, bytes):
            subject += part.decode(encoding or "utf-8", errors="ignore")
        else:
            subject += part

    body = ""

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(errors="ignore")
                break
    else:
        payload = email_message.get_payload(decode=True)
        if payload:
            body = payload.decode(errors="ignore")

    return {
        "from": sender,
        "subject": subject.strip(),
        "date": date,
        "content": body.strip()
    }
