# Generated by Django 5.0.4 on 2024-04-24 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_review_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='value',
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
