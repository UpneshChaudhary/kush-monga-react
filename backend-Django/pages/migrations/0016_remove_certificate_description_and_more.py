# Generated by Django 4.2.9 on 2024-02-21 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0015_remove_award_description_remove_award_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='description',
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='title',
        ),
    ]
