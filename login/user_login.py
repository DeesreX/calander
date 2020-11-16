#---# Print module loaded
print(f'Module [user_login] loaded.')

#---# All imports
import json, pickle, os, datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

#---# Functions
def login_user():
    while True:
        user_creds = load_data()
        u_input = input(f'Please enter your username: [username][back]\n > ')
        if not u_input: continue
        if u_input == 'back': break
        if (u_input + '@student.wethinkcode.co.za') not in user_creds['user']:
            print(f'User [{u_input}] does not exist.')
            continue


        creds = None    
        if os.path.exists(f'login/users/{u_input}@student.wethinkcode.co.za.pickle'):
            with open(f'login/users/{u_input}@student.wethinkcode.co.za.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
        service = build('calendar', 'v3', credentials=creds)
        print(f'User [{u_input}] has been logged in.')
        event = {'summary':'asd','start':{'dateTime':'2020-11-16T09:30+02:00'},'end':{'dateTime':'2020-11-16T10:00+02:00'}}
        service.events().insert(calendarId='primary',body=event).execute()

        return service


def create_new_user():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    user_creds = load_data()
    while True:
        u_input = input('Please enter your username : [username][back]\n > ')
        if not u_input: continue
        if u_input == 'back': break
        if (u_input + '@student.wethinkcode.co.za') in user_creds['user']:
            print(f'User [{u_input}] allready exists. New user has not been created.')
            continue 
        user_creds['user'].append(f'{u_input}@student.wethinkcode.co.za')
        with open('login/users/user_creds.json', 'w') as creds:
            json.dump(user_creds,creds)
        
        creds = None
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open(f'login/users/{u_input}@student.wethinkcode.co.za.pickle', 'wb') as token:
            pickle.dump(creds, token)
        break
    print(f'User [{u_input}@student.wethinkcode.co.za] has been created')


def load_data():
    with open('login/users/user_creds.json', 'r') as data:
        user_creds = json.load(data)
    return user_creds


def login_menu():
    while True:
        u_input = input(f'Please choose an option: [login][new][off]\n > ')
        if u_input == 'login': 
            service = login_user()
            break
        elif u_input == 'off': break
        elif u_input == 'new': create_new_user()
        else: print('Please select a valid option.')


def login_wtc():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    wtc_path = f'login/wtc/wtc.code.clinic@gmail.com.pickle'
    creds = None
    if os.path.exists(wtc_path):
        with open(wtc_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(wtc_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    print(f'WTC has been logged in.')
    return service

create_new_user()
login_user()