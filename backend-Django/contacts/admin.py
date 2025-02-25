from django import forms
from tinymce.widgets import TinyMCE
from django.contrib import admin
from django.shortcuts import render
from django.core.mail import send_mail
from .models import Contacts
from .models import MarketAppraisal, Registered_User
from django import forms
from .models import PropertyOffer
from .models import Old_Data_List


class MarketAppraisalAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'created_at']
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    list_filter = ['created_at']

admin.site.register(MarketAppraisal, MarketAppraisalAdmin)


class ContactsAdmin(admin.ModelAdmin):
    # ContactsAdmin configuration
    list_display = ('name', 'email', 'phone', 'listing')
    actions = ['send_bulk_email']  # Register the action
    search_fields = ['name']



class RegisteredUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'purpose')
    search_fields = ('name', 'email', 'phone')





class PropertyOfferAdmin(admin.ModelAdmin):
    list_display = ('buyer1', 'email_buyer1', 'purchase_price', 'property_address', 'contact_number', 'created_at')
    search_fields = ('buyer1', 'buyer2', 'email_buyer1', 'email_buyer2', 'property_address')
    list_filter = ('bank_borrowing_from', 'pre_approval', 'finance_approval_days', 'settlement_days')
    ordering = ('-created_at',)  # Order by the creation date



@admin.register(Old_Data_List)
class OldDataListAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'address', 'city')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'city')

admin.site.register(PropertyOffer, PropertyOfferAdmin)




admin.site.register(Registered_User, RegisteredUserAdmin)
admin.site.register(Contacts, ContactsAdmin)
