# Generated by Django 4.0.2 on 2022-02-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nobitex', '0004_trades_delete_trade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trades',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
