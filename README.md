<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title> Gmail to Google Sheets Automation </title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #222;
        }
        h1, h2, h3 {
            color: #0b5394;
        }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
        }
        pre {
            background: #f4f4f4;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
        }
        ul {
            margin-left: 20px;
        }
        table {
            border-collapse: collapse;
            margin-top: 10px;
        }
        table, th, td {
            border: 1px solid #aaa;
            padding: 8px;
        }
        th {
            background: #eaeaea;
        }
        .note {
            background: #fff3cd;
            padding: 10px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }
    </style>
</head>
<body>

<h1>Gmail to Google Sheets Automation</h1>

<p><strong>Author:</strong> Vaibhav<br>
<strong>Language:</strong> Python 3<br>
<strong>Type:</strong> Backend Automation Script</p>

<hr>

<h2>📌 Project Overview</h2>
<p>
This project is a Python-based automation system that reads <strong>real unread emails</strong>
from a Gmail inbox and logs them into a <strong>Google Sheet</strong>.
Each email is processed exactly once, appended as a new row, and then marked as read.
</p>

<p>
The system is designed to be <strong>secure</strong>, <strong>idempotent</strong>,
and <strong>production-safe</strong>, following Google API best practices.
</p>

<hr>

<h2>🏗 High-Level Architecture Diagram</h2>

<pre>
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
</pre>

<hr>

<h2>⚙️ Step-by-Step Setup Instructions</h2>

<h3>1. Clone the Repository</h3>
<pre><code>git clone &lt;your-repo-link&gt;
cd gmail-to-sheets</code></pre>

<h3>2. Create and Activate Virtual Environment</h3>
<pre><code>python -m venv venv
venv\Scripts\activate</code></pre>

<h3>3. Install Dependencies</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h3>4. Google Cloud Setup</h3>
<ul>
    <li>Create a Google Cloud Project</li>
    <li>Enable Gmail API and Google Sheets API</li>
    <li>Configure OAuth Consent Screen (External)</li>
    <li>Add your Gmail account as a Test User</li>
    <li>Create OAuth Client ID (Desktop App)</li>
</ul>

<h3>5. Add Credentials (DO NOT COMMIT)</h3>
<pre><code>credentials/credentials.json</code></pre>

<h3>6. Create Google Sheet</h3>
<ul>
    <li>Create a new Google Sheet</li>
    <li>Add headers in the first row:</li>
</ul>

<pre><code>From | Subject | Date | Content</code></pre>

<p>Copy the Spreadsheet ID and update <code>config.py</code>.</p>

<h3>7. Run the Script</h3>
<pre><code>python -m src.main</code></pre>

<hr>

<h2>🔐 OAuth Flow Used</h2>
<ul>
    <li>OAuth 2.0 Installed App Flow</li>
    <li>Browser-based user authentication</li>
    <li>Tokens stored locally and reused</li>
</ul>

<p>
Service accounts are not used because the Gmail API does not support them for personal inboxes.
</p>

<hr>

<h2>🔁 Duplicate Prevention Logic</h2>
<p>
Each Gmail email has a unique message ID.
After processing an email, its ID is stored locally.
If the script encounters the same ID again, it skips processing.
</p>

<p>This ensures safe re-runs and no duplicate rows.</p>

<hr>

<h2>💾 State Persistence Method</h2>
<p>
State is stored in a local file called <code>state.json</code>,
which contains all processed Gmail message IDs.
</p>

<ul>
    <li>Faster than checking Google Sheets</li>
    <li>Independent of output storage</li>
    <li>Offline-safe</li>
</ul>

<div class="note">
<strong>Note:</strong> Deleting Google Sheet data does not reset processing.
To reprocess emails intentionally, <code>state.json</code> must be deleted.
</div>

<hr>

<h2>🔐 Security Rules</h2>
<ul>
    <li><strong>credentials.json</strong> is never committed</li>
    <li><strong>token.json</strong> is never committed</li>
    <li><strong>state.json</strong> is never committed</li>
</ul>

<p>
These files are excluded using <code>.gitignore</code> to prevent credential leakage.
</p>

<hr>

<h2>🚧 Challenge Faced & Solution</h2>

<h3>Challenge</h3>
<p>
Some emails had very large bodies exceeding Google Sheets’
50,000-character cell limit.
</p>

<h3>Solution</h3>
<p>
Email content is truncated before insertion,
preventing crashes while preserving meaningful data.
</p>

<hr>

<h2>⚠️ Limitations of the Solution</h2>
<ul>
    <li>HTML-only emails may have limited plain-text content</li>
    <li>Email attachments are ignored</li>
    <li>State is stored locally (not shared across machines)</li>
    <li>Email body content is truncated to respect Sheets limits</li>
</ul>

<hr>

<h2>✅ Final Notes</h2>
<ul>
    <li>Only unread emails are processed</li>
    <li>Emails are marked as read after processing</li>
    <li>Re-running the script does not create duplicates</li>
    <li>Designed for security, clarity, and maintainability</li>
</ul>

</body>
</html>
