# Generated by Django 4.2.7 on 2024-01-01 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_remove_blog_read_more_link_blog_full_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.IntegerField()),
                ('review', models.TextField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
