# Generated by Django 5.1.5 on 2025-02-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_registration_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
