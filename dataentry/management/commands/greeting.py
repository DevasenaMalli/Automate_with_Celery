from typing import Any
from django.core.management.base import BaseCommand, CommandParser

class Command(BaseCommand):
    help = "Greets the user"

    def add_arguments(self,parser):
       parser.add_argument('name', type=str, help='specifies user name')

    def handle(self, *args, **kwargs):
      name = kwargs['name']
      greeting = f'hi {name}, good morning!!'
      self.stdout.write(self.style.SUCCESS(greeting))