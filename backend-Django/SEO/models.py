

from django.db import models

class MetaDescription(models.Model):
    PAGE_CHOICES = [
        ('index', 'Home'),
        ('listings', 'Listings'),
        ('coming_soon', 'Coming Soon'),
        ('about', 'About'),
        ('blog_list', 'Blogs'),
        ('sold_properties', 'Sold Properties'),
        ('testimonials', 'Testimonials'),
    ]

    page_name = models.TextField(choices=PAGE_CHOICES, unique=True)
    meta_description = models.TextField()

    def __str__(self):
        return f'{self.get_page_name_display()} - Meta Description'

    class Meta:
        verbose_name = 'Meta Description'
        verbose_name_plural = 'Meta Descriptions'
