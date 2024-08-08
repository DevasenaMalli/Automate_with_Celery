from awd_main.celery import app
import time
from django.core.management import call_command
from .utils import sen_email_notifications
import ssl
import certifi
from django.conf import settings

@app.task
def celery_test_task():
    time.sleep(5)        # simulation of any task that's going to take 10 sec

    #send an email
    mail_subject = 'Test subject'
    message = 'This is a test email'
    to_email = settings.DEFAULT_TO_EMAIL
    sen_email_notifications(mail_subject, message, to_email)
    return 'Email sent successfully'



@app.task
def import_data_task(file_path, model_name):
     try:
        call_command('importdata', file_path, model_name)
        
     except Exception as e:
           raise e
     #notify the use by email
     mail_subject = 'Import Data Completed'
     message = 'Your data imported has been successful'
     to_email = settings.DEFAULT_TO_EMAIL
     sen_email_notifications(mail_subject, message, to_email)

     return "Data imported successfully."