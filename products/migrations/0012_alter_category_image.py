# Generated by Django 5.0.4 on 2024-04-23 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='category_images'),
        ),
    ]