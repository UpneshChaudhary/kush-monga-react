# Generated by Django 4.2.9 on 2024-02-06 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_feedbackcard_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='textreview',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
    ]
