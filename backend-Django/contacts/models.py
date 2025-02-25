from django.db import models
from datetime import datetime

class Contacts(models.Model):
    listing = models.CharField(max_length=200)
    listing_id = models.IntegerField()
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.IntegerField(blank=True)
    source_of_Enquiry = models.CharField(max_length=200, default='website')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Enquiries"

class MarketAppraisal(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    street_address = models.CharField(max_length=255)
    suburb = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    cars = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "Market Appraisals"

class Registered_User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    purpose = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Registered Users"




class PropertyOffer(models.Model):
    property_address = models.CharField(max_length=200)
    buyer1 = models.CharField(max_length=200)
    email_buyer1 = models.EmailField()
    buyer2 = models.CharField(max_length=200, blank=True, null=True)
    email_buyer2 = models.EmailField(blank=True, null=True)
    current_address = models.CharField(max_length=200)
    bank_borrowing_from = models.CharField(max_length=100)
    percentage_borrowing_or_cash_offer = models.CharField(max_length=20)
    current_savings = models.CharField(max_length=200)
    broker_details = models.TextField()
    deposit_amount = models.CharField(max_length=200)
    finance_approval_days = models.CharField(max_length=20)
    settlement_days = models.CharField(max_length=20)
    purchase_price = models.CharField(max_length=200)
    pre_approval = models.CharField(max_length=20) # New field for pre-approval
    contact_number = models.CharField(max_length=15, default='123-456-7890')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer1} & {self.buyer2}" if self.buyer2 else self.buyer1


class Old_Data_List(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, default='0')
    address = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
