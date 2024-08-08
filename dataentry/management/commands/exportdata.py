import csv
from django.core.management.base import BaseCommand
#from dataentry.models import Student
from django.apps import apps
import datetime

from dataentry.utils import generate_csv_file

#proposed command = python3 manage.py exportdata model_name

class Command(BaseCommand):
    help = "Export data from student model to csv file"
    
    def add_arguments(self, parser):
       parser.add_argument('model_name', type=str, help='Model name')

    def handle(self, *args, **kwargs ):
        model_name = kwargs['model_name'].capitalize()
        

        #search through all the apps
        model = None
        for app_config in apps.get_app_configs():
          try:
              print(f"Searching in app: {app_config.label}")  # Debugging line

              model = app_config.get_model(model_name)
              if model_name in app_config.models:
                model = app_config.get_model(model_name)
                print(f"Model {model_name} found in app: {app_config.label}")  # Debugging line

                break
          except LookupError:
              continue
        if not model:
            self.stderr.write(self.style.ERROR(f'Model {model_name} not found'))
            return
        
        #fetct data from database
        data = model.objects.all()
        
        file_path = generate_csv_file(model_name)

        #generate the timestamp of current date and time
       
        #open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            #writer the csv header
            #we want to print field of model thet we are trying to export
            writer.writerow([field.name for field in model._meta.fields])
            #write data rows
            for obj in data:
                writer.writerow([getattr(obj, field.name) for field in model._meta.fields])
    
        self.stdout.write(self.style.SUCCESS('Data exported successfully!'))