# Gmail to Google Sheets Automation

**Author:** Vaibhav Kandpal  

**Language:** Python 3  
**Type:** Backend Automation Script

---

## 📌 Project Overview

This project is a Python-based automation system that reads **real unread emails** from a Gmail inbox and logs them into a **Google Sheet**. Each email is processed **exactly once**, appended as a new row, and then marked as **read**.

The system is designed to be **secure**, **idempotent**, and **production-safe**, following Google API best practices.

---

## 🏗 High-Level Architecture

```
+-------------------+
|   Gmail Inbox     |
| (Unread Emails)   |
+---------+---------+
          |
          | Gmail API (OAuth 2.0)
          v
+-------------------+
|  Python Script    |
|                   |
| - Auth Handler    |
| - Email Parser    |
| - State Manager   |
+---------+---------+
          |
          | Google Sheets API
          v
+-------------------+
| Google Sheet      |
| (Append-only)     |
+-------------------+
```

---

## ⚙️ Step-by-Step Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd gmail-to-sheets
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Google Cloud Setup

- Create a Google Cloud Project
- Enable Gmail API and Google Sheets API
- Configure OAuth Consent Screen (External)
- Add your Gmail account as a Test User
- Create OAuth Client ID (Desktop App)

### 5. Add Credentials (DO NOT COMMIT)

Place your downloaded credentials file at:

```
credentials/credentials.json
```

### 6. Create Google Sheet

- Create a new Google Sheet
- Add headers in the first row:

```
From | Subject | Date | Content
```

- Copy the Spreadsheet ID from the URL and update `config.py`

### 7. Run the Script

```bash
python -m src.main
```

---

## 🔐 OAuth Flow Used

- OAuth 2.0 Installed App Flow
- Browser-based user authentication
- Tokens stored locally and reused

> **Note:** Service accounts are not used because the Gmail API does not support them for personal inboxes.

---

## 🔁 Duplicate Prevention Logic

Each Gmail email has a unique message ID. After processing an email, its ID is stored locally. If the script encounters the same ID again, it skips processing.

This ensures safe re-runs and no duplicate rows.

---

## 💾 State Persistence Method

State is stored in a local file called `state.json`, which contains all processed Gmail message IDs.

**Advantages:**
- Faster than checking Google Sheets
- Independent of output storage
- Offline-safe

> **Important:** Deleting Google Sheet data does not reset processing. To reprocess emails intentionally, `state.json` must be deleted.

---

## 🔐 Security Rules

The following files are **never committed** to version control:

- `credentials.json` - OAuth client credentials
- `token.json` - User access tokens
- `state.json` - Processing state

These files are excluded using `.gitignore` to prevent credential leakage.

---

## 🚧 Challenge Faced & Solution

### Challenge
Some emails had very large bodies exceeding Google Sheets' 50,000-character cell limit.

### Solution
Email content is truncated before insertion, preventing crashes while preserving meaningful data.

---

## ⚠️ Limitations of the Solution

- HTML-only emails may have limited plain-text content
- Email attachments are ignored
- State is stored locally (not shared across machines)
- Email body content is truncated to respect Sheets limits

---

## ✅ Final Notes

- Only unread emails are processed
- Emails are marked as read after processing
- Re-running the script does not create duplicates
- Designed for security, clarity, and maintainability

---



## 📧 Contact

For questions or issues, please contact [iamvaibhav192@gmail.com]
