# Generated by Django 4.2.7 on 2023-12-18 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0002_realtor_hire_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realtor',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
