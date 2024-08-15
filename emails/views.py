from django.shortcuts import render,redirect

from .task import send_email_task

from .models import Subcriber
from .forms import EmailForm
from django.contrib import messages
from django.conf import settings
from dataentry.utils  import send_email_notifications

# Create your views here.

def send_email(request):
    if request.method == "POST":
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            #sending email
            mail_subject = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            #access the selected email list
            email_list = email_form.email_list

            #extract email adress from the subsriber model
            subcribers = Subcriber.objects.filter(email_list=email_list)

            to_email = []
            for email in subcribers:
                to_email.append(email.email_adress)
            
            if email_form.attachment:
                attachment = email_form.attachment.path
            else:
                 attachment = None
            #handover email task to celery
            send_email_task.delay(mail_subject, message, to_email, attachment)

            #display a success message
            messages.success(request, 'Email sent successfully!')
            return redirect('send_email')
    else:
        email_form = EmailForm()
        context = {
            'email_form': email_form
        }
    return render(request, 'emails/send-email.html', context)