from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import time
import math



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']


def getCreds():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/r/Downloads/client_secret_803618097882-82qgfndaha92hch7j9l7f62i3e89itvu.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # service = build('calendar', 'v3', credentials=creds)
    #
    # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    #
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    #
    # calendar_list_entry = service.calendarList().get(calendarId='primary').execute()
    #
    # print ("calendar access auth")
    # print (calendar_list_entry['summary'])
    return creds

my_tz = 'America/Los_Angeles'
last_event_id = ""
lastWorkTime = False
laststuff = {}
color = "4"

def addEvent(stuff):
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/r/Downloads/Quickstart-e675ca2d25d8.json"

    # this string will have our description
    desc = ""

    # loop through the dictionary that maps the category/app to the time
    isWorking = 0
    notWorking = 0
    for k, v in stuff.items():
        # add in key and value with a newline
        if len(k) >= 6 and 'Games' in k:
            notWorking+=1
        else:
            isWorking+=1
        desc+=f"{k}: {v}\n"
    #start time in epochs
    dts = int(time.time())
    #end date time in epochs
    dte = dts-300
    # creating the event json payload
    status = "Off Task"
    global worktime
    worktime = False
    global color
    if isWorking > notWorking:
        worktime = True
        status = "On Task"
        color = "2"
    event = {
        'summary': f"Project Aim: {status}",
        'location': '2844 Ramona Street, Palo Alto, CA',
        'description': desc,
        'start': {
            'dateTime': datetime.datetime.fromtimestamp(dte).isoformat("T"),
            'timeZone': my_tz,
        },
        'end': {
            'dateTime': datetime.datetime.fromtimestamp(dts).isoformat("T"),
            'timeZone': my_tz,
        },
        'colorId': color,
    }
    global lastWorkTime
    global last_event_id
    service = build('calendar', 'v3', credentials=getCreds())
    if worktime == lastWorkTime and last_event_id != "":
        lastWorkTime = worktime
        desc = ""
        global laststuff
        laststuff.update(stuff)
        for k, v in laststuff.items():
            # add in key and value with a newline
            if len(k) >= 6 and 'Games' in k:
                notWorking += 1
            else:
                isWorking += 1
            desc += f"{k}: {v}\n"
        print(last_event_id)
        retevent = service.events().get(calendarId='primary', eventId=last_event_id).execute()
        retevent['description'] = desc
        retevent['end']['dateTime'] = datetime.datetime.fromtimestamp(dts).isoformat("T")
        updatedevent = service.events().update(calendarId='primary', eventId=retevent['id'], body=retevent).execute()
        last_event_id = updatedevent["id"]
    else:
        retevent = service.events().insert(calendarId='primary', body=event).execute()
        last_event_id = retevent["id"]
        laststuff = stuff
    lastWorkTime = worktime

