# Generated by Django 5.0.2 on 2024-05-22 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BusManagement_App', '0003_auto_20240520_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='Sex',
            field=models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M', help_text='Votre identité Sexuel', max_length=10),
        ),
        migrations.AddField(
            model_name='parent',
            name='Sex',
            field=models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M', help_text='Votre identité Sexuel', max_length=10),
        ),
        migrations.AddField(
            model_name='student',
            name='Sex',
            field=models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], default='M', help_text='Votre identité Sexuel', max_length=10),
        ),
    ]
