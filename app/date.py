from __future__ import print_function
from datetime import datetime
import dateutil.parser
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def getInfo():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'app.credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    info=[]
    if not events:
        print('No upcoming events found.')
    for event in events:

        start = event['start'].get('dateTime', event['start'].get('date'))
        end =event['end'].get('dateTime',event['end'].get('date'))

        startTime=dateutil.parser.parse(start)
        startTime=(startTime.time())

        endTime=dateutil.parser.parse(end)
        endTime=(endTime.time())

        datetime_object = dateutil.parser.parse(start)
        datetime_object = datetime_object.date()

        todayDate=(datetime.today())
        todayDate=todayDate.strftime("%Y-%m-%d")
        todayDate=dateutil.parser.parse(todayDate)
        todayDate=todayDate.date()
        if datetime_object==todayDate:
            info.append((todayDate, startTime, endTime,event['summary']))
    return info
print(getInfo())
