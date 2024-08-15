from django.contrib import admin
from . models import List,Subcriber,Email

# Register your models here.

admin.site.register(List)
admin.site.register(Subcriber)
admin.site.register(Email)