from django.contrib import admin
from .models import MissingChild, FoundPerson

# Register your models here.
admin.site.register(MissingChild)
admin.site.register(FoundPerson)