# Generated by Django 4.0.2 on 2022-02-05 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nobitex', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='market',
            unique_together={('base_asset', 'quote_asset')},
        ),
    ]