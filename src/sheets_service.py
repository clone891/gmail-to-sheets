from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import pickle
import os

from config import TOKEN_PATH, SHEETS_SCOPES
from config import SPREADSHEET_ID, SHEET_RANGE


def append_row(service, row_values):
    body = {
        "values": [row_values]
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_RANGE,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
    
def get_sheets_service():
    if not os.path.exists(TOKEN_PATH):
        raise Exception("token.json not found. Run Gmail auth first.")

    with open(TOKEN_PATH, "rb") as token:
        creds = pickle.load(token)

    service = build("sheets", "v4", credentials=creds)
    return service
