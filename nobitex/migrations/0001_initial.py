# Generated by Django 4.0.2 on 2022-02-05 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_asset', models.CharField(max_length=8)),
                ('quote_asset', models.CharField(max_length=8)),
            ],
        ),
    ]