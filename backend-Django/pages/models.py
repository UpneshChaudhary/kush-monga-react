# models.py
from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
import itertools
from ckeditor.fields import RichTextField
from listings.models import Listing 

def validate_file_extension(value):
    if not value.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
        raise ValidationError('Only PDF, JPG, JPEG, and PNG files are allowed.')




class SoldProperty(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    price = models.CharField(max_length=40)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField(default=2)
    sqft = models.IntegerField()
    image1 = models.ImageField(upload_to='sold_images/')
    image2 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image6 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image7 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image8 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image9 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    image10 = models.ImageField(upload_to='sold_images/', blank=True, null=True)
    video = models.URLField(blank=True, default='https://www.example.com/default-video-url')
    floor_plan = models.FileField(
        upload_to='floor_plans/%Y/%m/%d',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    garage = models.IntegerField(default=2)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = original_slug = slugify(self.title)
            for x in itertools.count(1):
                if not SoldProperty.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{original_slug}-{x}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('sold_property_detail', args=[self.slug])

    def transfer_from_listing(self, listing):
        """Transfer data from a Listing instance to this SoldProperty."""
        if not isinstance(listing, Listing):
            raise ValueError("Expected a Listing instance.")

        self.title = listing.title
        self.address = listing.address
        self.city = listing.city
        self.state = listing.state
        self.zipcode = listing.zipcode
        self.description = listing.description
        self.price = listing.price
        self.bedrooms = listing.bedrooms
        self.bathrooms = listing.bathrooms
        self.sqft = listing.sqft
        self.garage = listing.garage
        
        # Map Listing photo fields to SoldProperty image fields
        self.image1 = listing.photo_main  # Assuming this maps to the main photo
        self.image2 = listing.photo_1
        self.image3 = listing.photo_2
        self.image4 = listing.photo_3
        self.image5 = listing.photo_4
        self.image6 = listing.photo_5
        self.image7 = listing.photo_6
        self.image8 = listing.photo_7
        self.image9 = listing.photo_8
        self.image10 = listing.photo_9
        
        # Continue mapping if needed
        # You can add more images if your SoldProperty model has more fields.

        if listing.video:
            self.video = listing.video
        if listing.floor_plan:
            self.floor_plan = listing.floor_plan

        self.listing = listing  # Link to the original listing

        # Automatically generate a unique slug
        self.slug = original_slug = slugify(self.title)
        for x in itertools.count(1):
            if not SoldProperty.objects.filter(slug=self.slug).exists():
                break
            self.slug = f'{original_slug}-{x}'

        self.save()



class Certificate(models.Model):
    title = models.CharField(max_length=255, default="Default Title")
    description = models.TextField(default="Default Description")
    image = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return self.title


class Award(models.Model):
    title = models.CharField(max_length=255, default="Default Title")
    #description = models.TextField()
    image = models.ImageField(upload_to='awards/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class About(models.Model):
    agent_image = models.ImageField(upload_to='about_images/')
    background_image = models.ImageField(upload_to='about_images/')
    logo_image = models.ImageField(upload_to='about_images/')
    background_image2 = models.ImageField(upload_to='about_images/')
    ppre_logo = models.ImageField(upload_to='about_images/', default='about_images/default_logo.jpg')
    logo_icon = models.ImageField(upload_to='about_images/', default='about_images/default_logo.jpg')
    background_image3 = models.ImageField(upload_to='about_images/', default='about_images/default_logo.jpg')


    def __str__(self):
        return "About Section"


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    full_content = models.TextField(default='full_content')
    image = models.ImageField(upload_to='blog_images/')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.pk])


class TextReview(models.Model):
    stars = models.IntegerField()
    review = models.TextField()
    name = models.TextField(default="Default Name")
    email = models.EmailField(default="example@example.com")  # Adding email field
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stars} stars - {self.review[:20]}..."




class FeedbackCard(models.Model):
    title = models.CharField(max_length=255)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    garage = models.PositiveIntegerField(default="0")
    photo = models.ImageField(upload_to='feedback_photos/')  # Assuming you have an 'uploads' directory
    #star_ratings = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    star_ratings = models.IntegerField()
    empty_stars = models.PositiveIntegerField()  # Assuming this field indicates the number of empty stars
    review_title = models.CharField(max_length=255)
    review_detail = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    Owner = models.CharField(max_length=100,default='None')

    def __str__(self):
        return self.title
