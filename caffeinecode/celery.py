import os

from celery import Celery
from dotenv import load_dotenv
load_dotenv()  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'caffeinecode.settings')

app = Celery('caffeinecode',broker=os.environ.get("REDIS_BROKER_URL"))
app.conf.task_ignore_result = True
app.conf.timezone = "Asia/Kolkata"
app.conf.update(CELERY_REDIS_MAX_CONNECTIONS = 20,)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

