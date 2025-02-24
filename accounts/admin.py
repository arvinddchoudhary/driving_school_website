from django.contrib import admin # type: ignore

# Register your models here.
from .models import Registration

admin.site.register(Registration)