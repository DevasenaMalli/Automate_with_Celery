from django.core.management.base import BaseCommand, CommandParser,CommandError
#from dataentry.models import Student
from django.apps import apps
import csv

from django.db import DataError

#proposed command - python manage.py importdata file_path model_name

class Command(BaseCommand):
    help = "Import data from CSV file"

    def add_arguments(self, parser):
      #logic goes here
      parser.add_argument('file_path',type=str, help='Path to the CSV file')
      parser.add_argument('model_name',type=str, help='Name of model')
     

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()

         #search for the model across all installed apps
        model = None
        for app_config in apps.get_app_configs():
           #try to search for the model
           try:
            model = apps.get_model(app_config.label,model_name)
            break #stop searching once the model is found
           except LookupError:
              continue
           
        if not model:
           raise CommandError(f'Model "{model_name}" not found in any app!')
        #get all the field names of the model that we found
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        print(model_fields)

        with open(file_path, 'r') as file:
           reader = csv.DictReader(file)
           csv_header = reader.fieldnames

           #compare csv header with model's field names
           if csv_header != model_fields:
              raise DataError(f" CSV file doesn't match with the {model_name} table field. ")
           for row in reader:
              model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data imported from csv successfully"))