#---# Print module loaded
print(f'Module [events] loaded.')

#---# All imports
import datetime

#---# Functions

def create_event(summary, date, time):
    full_time = datetime.datetime(
        int(date.split('-')[0]),
        int(date.split('-')[1]),
        int(date.split('-')[2]),
        int(time.split(':')[0]),
        int(time.split(':')[1])
    )
    duration = full_time + datetime.timedelta(minutes=30)
    event = {
        'summary':summary,
        'start': {
            'dateTime': f'{date}T{time}+02:00'
        },
        'end': {
            'dateTime': f'{date}T{duration.time()}+02:00'
        }
    }
    return event


def insert_event(service, event):
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(event)

def delete_event():
    pass


def update_event():
    pass


def add_email():
    pass

create_event('test','2020-11-16','9:30')
