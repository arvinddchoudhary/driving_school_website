from django.db import models # type: ignore

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class FaqItem(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class Home(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='home_images/')

    def __str__(self):
        return self.title
    

class Instructors(models.Model):
    name = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()  # years of experience
    specialization = models.CharField(max_length=255)
    description = models.TextField()  # A field for a detailed description
    image = models.ImageField(upload_to='instructors/')

    def __str__(self):
        return self.name
