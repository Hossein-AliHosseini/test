# Generated by Django 4.0.2 on 2022-03-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='field',
            field=models.CharField(max_length=20),
        ),
    ]
