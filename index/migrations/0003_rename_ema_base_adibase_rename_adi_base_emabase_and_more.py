# Generated by Django 4.0.2 on 2022-03-06 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nobitex', '0008_rename_trades_trade'),
        ('index', '0002_remove_ma_period_end'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EMA_Base',
            new_name='ADIBase',
        ),
        migrations.RenameModel(
            old_name='ADI_Base',
            new_name='EMABase',
        ),
        migrations.RenameModel(
            old_name='MA_Base',
            new_name='MABase',
        ),
        migrations.RenameModel(
            old_name='SO_Base',
            new_name='SOBase',
        ),
    ]
