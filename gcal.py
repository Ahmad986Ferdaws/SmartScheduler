# app/gcal.py

from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

# Load credentials from your Google Service Account JSON
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service_account.json'  # Path to your credentials

def create_gcal_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, calendar_id, event):
    start_datetime = datetime.datetime.strptime(event['start_time'], '%Y-%m-%dT%H:%M:%S')
    end_datetime = start_datetime + datetime.timedelta(minutes=event['duration_mins'])

    event_body = {
        'summary': event['title'],
        'description': event.get('notes', ''),
        'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'UTC'},
        'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'UTC'},
    }

    created_event = service.events().insert(calendarId=calendar_id, body=event_body).execute()
    return created_event.get('htmlLink')
