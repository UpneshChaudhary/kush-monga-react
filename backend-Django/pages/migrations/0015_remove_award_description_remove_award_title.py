# Generated by Django 4.2.9 on 2024-02-21 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_textreview_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='award',
            name='description',
        ),
        migrations.RemoveField(
            model_name='award',
            name='title',
        ),
    ]
