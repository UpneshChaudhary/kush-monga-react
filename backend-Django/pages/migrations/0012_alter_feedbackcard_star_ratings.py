# Generated by Django 4.2.7 on 2024-01-27 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_alter_feedbackcard_garage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackcard',
            name='star_ratings',
            field=models.IntegerField(),
        ),
    ]
