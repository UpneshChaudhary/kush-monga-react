# Generated by Django 4.2.9 on 2024-08-18 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0016_listing_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listing',
            options={'verbose_name_plural': 'Listings'},
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_1',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_10',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_11',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_12',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_13',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_14',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_15',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_16',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_17',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_18',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_2',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_3',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_4',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_5',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_6',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_7',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_8',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='photo_9',
        ),
    ]
