# Generated by Django 5.1.5 on 2025-01-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_feature_testimonial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='image_url',
        ),
        migrations.AddField(
            model_name='feature',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='features/'),
        ),
    ]
