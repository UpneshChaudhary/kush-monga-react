# Generated by Django 4.2.9 on 2024-04-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_alter_contacts_options_alter_marketappraisal_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contacts',
            options={'verbose_name_plural': 'Enquiries'},
        ),
        migrations.AddField(
            model_name='contacts',
            name='source_of_Enquiry',
            field=models.CharField(default='website', max_length=200),
        ),
    ]
