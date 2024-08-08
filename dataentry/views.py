from django.shortcuts import render,redirect
from .utils import check_csv_errors, get_all_custom_models
from uploads.models import Uploads
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages
from .tasks import import_data_task

# Create your views here.
def import_data(request):
     if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
     
        #store this file inside the upload model
        upload = Uploads.objects.create(file=file_path, model_name=model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        file_path= base_url+relative_path
        print(file_path)

        #check for the errors
        try:

          model = check_csv_errors(file_path, model_name)
        except Exception as e:
           messages.error(request, e)
           return redirect('import_data')

        #handle the import data task here
        import_data_task.delay(file_path, model_name)

        #show the message to the use
        messages.success(request, "Your data is being imported, you will be notified once it is done. ")
        return redirect('import_data')
     else:
        custom_models = get_all_custom_models()
        context = {
            'custom_models':custom_models,
        }

     return render(request, 'dataentry/importdata.html',context)