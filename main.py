from login import user_login
from api_funtions import events

# service = user_login.login_menu()
service = user_login.login_user()
event = events.create_event('test','2020-11-16','9:30')
events.insert_event(service,event)
