from django.db import models
from django.utils.text import slugify
import itertools
from datetime import datetime
from realtors.models import Realtor
from .utils import generate_qr_code
from contacts.models import Registered_User, Contacts
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from django.conf import settings
import logging
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import qrcode
from django.core.validators import FileExtensionValidator

def validate_file_extension(value):
    if not value.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
        raise ValidationError('Only PDF, JPG, JPEG, and PNG files are allowed.')


logger = logging.getLogger(__name__)


def validate_image_size(value):
    limit_mb = 5
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(gtl('Image size cannot exceed 5 MB').format(limit=limit_mb))



class Listing(models.Model):
    realtor = models.ForeignKey(Realtor, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)  # Corrected 'maxlength' to 'max_length'
    description = models.TextField(blank=True)
    price = models.CharField(max_length=40)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField(default=2)
    garage = models.IntegerField(default=2)
    sqft = models.IntegerField()
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d', validators=[validate_image_size])
    floor_plan = models.FileField(
        upload_to='floor_plans/%Y/%m/%d',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        blank=True,
        default='floor_plans/default/default-floor-plan.pdf'
    )
    video = models.URLField(blank=True)
    home_open = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)
    list_data = models.DateTimeField(default=datetime.now, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_7 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_8 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_9 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_10 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_11 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_12 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_13 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_14 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_15 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_16 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_17 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])
    photo_18 = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, validators=[validate_image_size])

    class Meta:
        verbose_name_plural = "Listing"

    def save(self, *args, **kwargs):
        # Generate unique slug if it doesn't exist
        if not self.slug:
            self.slug = original_slug = slugify(self.title)
            for x in itertools.count(1):
                if not Listing.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{original_slug}-{x}'
        
        super().save(*args, **kwargs)  # First save to generate the instance ID if needed

        # Generate QR code if it doesn't exist
        if not self.qr_code:
            qr_code_data = self.slug  # Use slug for QR code data
            qr_code_image = generate_qr_code(qr_code_data)
            self.qr_code.save(f"qr_code_{self.slug}.png", qr_code_image, save=False)
            super().save(*args, **kwargs)  # Save again to update the QR code field





class ComingSoon(models.Model):
    title = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='coming_soon_images/')
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    carspace = models.PositiveIntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else 'Coming Soon Item'

class Home_Open_Enquiries(models.Model):
    Property = models.CharField(max_length=200, default="", blank=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    #user_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Home_Open_Enquiries"



class Inspection(models.Model):
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"Inspection scheduled for {self.date} at {self.time}"


class UnsubscribedEmail(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email





class HomeOpen(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='home_opens', null=True)  # Link to Listing
    image = models.ImageField(upload_to='home_open_images/')
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    date = models.DateField()
    day = models.CharField(max_length=10, blank=True)  # Day of the week
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        # Automatically calculate and store the day based on the date
        self.day = self.date.strftime('%A')
        super(HomeOpen, self).save(*args, **kwargs)

    def has_expired(self):
        now = datetime.now()
        event_end_datetime = datetime.combine(self.date, self.end_time)
        return now > event_end_datetime

    def __str__(self):
        return self.title
