# Generated by Django 5.2.1 on 2025-05-20 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expensess', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=6),
        ),
    ]
