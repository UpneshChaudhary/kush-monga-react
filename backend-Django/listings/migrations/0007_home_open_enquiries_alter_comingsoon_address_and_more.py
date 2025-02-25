# Generated by Django 4.2.9 on 2024-03-23 14:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0006_comingsoon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Home_Open_Enquiries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Property', models.CharField(blank=True, default='31 Pegus Way', max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('message', models.TextField(blank=True)),
                ('contact_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.AlterField(
            model_name='comingsoon',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='comingsoon',
            name='area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comingsoon',
            name='bathrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comingsoon',
            name='bedrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comingsoon',
            name='carspace',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comingsoon',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
