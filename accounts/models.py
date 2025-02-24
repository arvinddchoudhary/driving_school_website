from django.db import models # type: ignore


class Registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=50)
    start_date = models.DateField()
    time_slot = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.course}"