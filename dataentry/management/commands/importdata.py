from django.core.management.base import BaseCommand, CommandParser,CommandError
#from dataentry.models import Student
from django.apps import apps
import csv

from django.db import DataError

from dataentry.utils import check_csv_errors

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


        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:
           reader = csv.DictReader(file)
       
           for row in reader:
              model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data imported from csv successfully"))