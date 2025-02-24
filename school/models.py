from django.db import models # type: ignore

class Course(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    image_url = models.URLField(blank=True, null=True)  # Store S3 image URL

    def _str_(self):
        return self.name

class FaqItem(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def _str_(self):
        return self.question

class Home(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)  # Store S3 image URL

    def _str_(self):
        return self.title

class Instructors(models.Model):
    name = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()
    specialization = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)  # Store S3 image URL

    def _str_(self):
        return self.name