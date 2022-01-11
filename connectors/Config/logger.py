from django.conf import settings
import datetime


def serverLogger(status,message):
    if settings.SERVER_LOGGER:
        if status =="success":
            print(f'✅ {datetime.datetime.now()}          {status}          {message}')
        else:
            print(f'❎ {datetime.datetime.now()}          {status}          {message}')