# Generated by Django 5.0.4 on 2024-05-11 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fav_products', '0003_alter_favoriteproducts_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteproducts',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, to='fav_products.favitem'),
        ),
    ]
