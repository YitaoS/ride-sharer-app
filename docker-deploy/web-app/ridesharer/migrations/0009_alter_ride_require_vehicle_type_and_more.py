# Generated by Django 4.1.5 on 2023-02-04 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ridesharer', '0008_alter_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='require_vehicle_type',
            field=models.CharField(blank=True, choices=[('S', 'SUV'), ('M', 'MiniBus'), ('B', 'Baby Car'), ('N', 'Normal Car')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_type',
            field=models.CharField(choices=[('S', 'SUV'), ('M', 'MiniBus'), ('B', 'Baby Car'), ('N', 'Normal Car')], default='N', max_length=1),
        ),
    ]
