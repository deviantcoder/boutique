# Generated by Django 5.0.4 on 2024-05-19 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_images/profile_default.png', upload_to='profile_images'),
        ),
    ]
