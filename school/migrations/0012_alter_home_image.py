# Generated by Django 5.1.5 on 2025-02-01 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0011_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='image',
            field=models.ImageField(upload_to='home_images/'),
        ),
    ]
