from django.urls import reverse
from django.contrib.sitemaps import Sitemap
from .models import Listing, ComingSoon

class ListingSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Listing.objects.filter(is_published=True)  # Only include published listings

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()