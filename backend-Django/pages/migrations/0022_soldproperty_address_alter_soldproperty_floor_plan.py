# Generated by Django 4.2.9 on 2024-03-07 00:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0021_soldproperty_garage_alter_soldproperty_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldproperty',
            name='address',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='soldproperty',
            name='floor_plan',
            field=models.FileField(blank=True, upload_to='floor_plans/%Y/%m/%d', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]),
        ),
    ]
