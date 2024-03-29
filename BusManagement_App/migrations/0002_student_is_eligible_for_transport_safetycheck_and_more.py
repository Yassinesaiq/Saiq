# Generated by Django 5.0.2 on 2024-02-25 16:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusManagement_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_eligible_for_transport',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='SafetyCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_date', models.DateField()),
                ('is_passed', models.BooleanField(default=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='safety_checks', to='BusManagement_App.bus')),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='BusManagement_App.route')),
            ],
        ),
        migrations.CreateModel(
            name='SecondaryAddressRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('is_approved', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondary_address_requests', to='BusManagement_App.student')),
            ],
        ),
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=6)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarifs', to='BusManagement_App.route')),
            ],
        ),
    ]
