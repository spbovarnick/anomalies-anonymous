from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'google-keys.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.json.

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1gYtaQG9jTyDPyVBL05yhOHDDwGcwSG2plYfftSDykoU'


service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="sightings-cleaned!A1:H65102").execute()
values = result.get('values', [])

print(values)