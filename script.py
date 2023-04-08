# This API call developed from Google documentation ( https://developers.google.com/sheets/api/quickstart/python ), this youtube video ( https://www.youtube.com/watch?v=4ssigWmExak ) and a couple ChatGPT queries to figure out how to: 1) clean up the data returned from the API; and 2) instantiate Sighting from the API 


from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account

import django
django.setup()
from main_app.models import Sighting
# from django.apps import apps

# SightingModel = apps.get_model('main_app', 'Sighting')

SERVICE_ACCOUNT_FILE = 'google-api.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.json.

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '15M468Vj9MKeszfqrCkE0tOObP0Xejv6lsGOPYF0n6CU'


service = build('sheets', 'v4', credentials=creds)

# Call the sheets API through google's service object and spreadsheets method
sheet = service.spreadsheets()
# values() returns values of sheet object, get calls down data from our spreadsheet, execute() sends request to API
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="sightings-cleaned!A1:H65102").execute()
# grab valid data from query in the result variable
values = result.get('values', [])

# removes column headers from values list
# keys are column headers
keys = values.pop(0)
# create new list named data where each row from sheet becomes dict
data = [dict(zip(keys, row)) for row in values]

for row in data:
    # **row passes key value pairs from data dictionaries as kwargs
    instance = Sighting(**row)
    instance.save()