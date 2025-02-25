# Generated by Django 4.2.7 on 2024-02-01 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_marketappraisal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Registered_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('purpose', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
                ('description', models.TextField()),
            ],
        ),
    ]
