from django.contrib import admin # type: ignore
from .models import Course, FaqItem, Home,Instructors

admin.site.register(Course)
admin.site.register(FaqItem)
admin.site.register(Home)
admin.site.register(Instructors)

