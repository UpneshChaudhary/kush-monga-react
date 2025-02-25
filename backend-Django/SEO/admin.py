

from django.contrib import admin
from .models import MetaDescription

@admin.register(MetaDescription)
class MetaDescriptionAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'meta_description')
    search_fields = ('page_name', 'meta_description')
