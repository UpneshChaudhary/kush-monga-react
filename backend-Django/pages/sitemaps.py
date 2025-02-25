from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from .models import Blog, SoldProperty  # Import your models here

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['index', 'about', 'blog_list', 'sold_properties', 'testimonials']

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

class SoldPropertySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return SoldProperty.objects.all()
