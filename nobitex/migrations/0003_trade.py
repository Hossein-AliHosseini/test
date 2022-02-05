# Generated by Django 4.0.2 on 2022-02-05 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nobitex', '0002_alter_market_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('price', models.FloatField()),
                ('volume', models.FloatField()),
                ('type', models.CharField(max_length=1)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nobitex.market')),
            ],
        ),
    ]
