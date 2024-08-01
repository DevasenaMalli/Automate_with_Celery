from django.core.management.base import BaseCommand
from  dataentry.models import Student


class Command(BaseCommand):
    help = "It will insert data to the database"

    def handle(self, *args, **kwargs):
        #logic goes here
        dataset = [
            {'roll_num':1002, 'name':'John', 'age':25},
            {'roll_num':1005, 'name':'Joseph', 'age':28},
            {'roll_num':1006, 'name':'Michel', 'age':29}
        ]
        
        for data in dataset:
          roll_num = data['roll_num']
          existing_record = Student.objects.filter(roll_num=roll_num).exists()
          if not existing_record:
            Student.objects.create(roll_num=data['roll_num'], name=data['name'], age=data['age'])
          else:
             self.stdout.write(self.style.WARNING(f'Student with the roll no {roll_num} already exists!'))
             
        self.stdout.write(self.style.SUCCESS('Data inserted successfully'))