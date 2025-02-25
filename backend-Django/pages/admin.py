
from django.contrib import admin
from django.db import models
from .models import SoldProperty, Certificate, Award, About, Blog
from .models import TextReview, FeedbackCard
from ckeditor.widgets import CKEditorWidget
from django.utils.text import slugify
import itertools



class SoldPropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    actions = ['generate_slugs']

    def generate_slugs(self, request, queryset):
        for property in queryset:
            if not property.slug:
                original_slug = slugify(property.title)
                slug = original_slug
                for x in itertools.count(1):
                    if not SoldProperty.objects.filter(slug=slug).exists():
                        break
                    slug = f'{original_slug}-{x}'
                property.slug = slug
                property.save()
        self.message_user(request, "Slugs have been generated for selected properties.")

    generate_slugs.short_description = "Generate slugs for selected properties"


    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
    list_display = (
        'title', 
        'address', 
        'price', 
        'bedrooms', 
        'bathrooms', 
        'sqft', 
        'garage', 
        'created_at'
    )
    list_filter = ('bedrooms', 'bathrooms', 'garage', 'created_at')
    search_fields = ('title', 'address', 'price')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'address', 'description', 'price', 'slug')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'sqft', 'garage')
        }),
        ('Media', {
            'fields': (
                'image1', 
                'image2', 
                'image3', 
                'image4', 
                'image5', 
                'image6', 
                'image7', 
                'image8', 
                'image9', 
                'image10', 
                'video'
            ),
        }),
        ('Floor Plan', {
            'fields': ('floor_plan',)
        }),
        ('Important Dates', {
            'fields': ('created_at',)
        }),
    )
    # To manage and display images in the admin
    def get_image(self, obj):
        return obj.image1.url if obj.image1 else None
    get_image.short_description = 'Image'
    get_image.allow_tags = True

    # Enable inline editing for images
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

# Optionally, add custom admin actions here





class AwardAdmin(admin.ModelAdmin):
    list_display = ('created_at',)
    search_fields = ('created_at',)

class TextReviewAdmin(admin.ModelAdmin):
    list_display = ('stars', 'review', 'name', 'email')
    search_fields = ('review',)
    list_filter = ('stars', 'uploaded_at', 'email')
    ordering = ('-uploaded_at',)



class FeedbackCardAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
    list_display = ('title', 'bedrooms', 'bathrooms', 'garage', 'star_ratings', 'review_title')
    search_fields = ('title', 'review_title')


class BlogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

admin.site.register(Blog, BlogAdmin)

admin.site.register(FeedbackCard, FeedbackCardAdmin)

admin.site.register(TextReview, TextReviewAdmin)



admin.site.register(SoldProperty, SoldPropertyAdmin)

admin.site.register(Certificate)

admin.site.register(Award, AwardAdmin)

admin.site.register(About)