# Generated by Django 5.0.4 on 2024-05-07 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_regular_customer',
            field=models.BooleanField(default=False, verbose_name='is_regular_customer'),
        ),
    ]
