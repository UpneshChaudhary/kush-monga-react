import os
from django.contrib import admin
from django.utils.html import format_html
from collections import Counter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.db import models
from django.http import HttpResponse
from django.urls import reverse
from .models import Listing, Home_Open_Enquiries, ComingSoon, HomeOpen, UnsubscribedEmail
from contacts.models import Contacts
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from ckeditor.widgets import CKEditorWidget
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate, 
    Paragraph, 
    Spacer, 
    Image, 
    Table, 
    TableStyle, 
    PageBreak
)


# Define file paths for the icons
price_icon_path = static('img/price_icon.png')
home_open_icon_path = static('img/home_open.png')

# Load price_icon with error handling
price_icon = ImageReader(price_icon_path) if os.path.exists(price_icon_path) else None
home_open_icon = ImageReader(home_open_icon_path) if os.path.exists(home_open_icon_path) else None

def draw_bar_graph(home_open_count, contacts_count, home_open_label, contacts_label, c, x, y):
    fig, ax = plt.subplots()
    labels = [home_open_label, contacts_label]
    counts = [home_open_count, contacts_count]
    ax.bar(labels, counts)
    ax.set_title("Combined Data")

    chart_output = BytesIO()
    plt.savefig(chart_output, format='png')
    plt.close()

    chart_output.seek(0)
    c.drawImage(ImageReader(chart_output), x, y, width=350, height=200, preserveAspectRatio=True)

def draw_pie_chart(home_open_count, contacts_count, c, x, y):
    labels = ["Home Open Enquiries", "Website Enquiries"]
    sizes = [home_open_count, contacts_count]
    colors = ['blue', 'green']

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
    ax.set_title("Distribution of Home Open and Website Enquiries")

    chart_output = BytesIO()
    plt.savefig(chart_output, format='png')
    plt.close()

    chart_output.seek(0)
    c.drawImage(ImageReader(chart_output), x, y, width=350, height=200, preserveAspectRatio=True)

class ListingAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
    list_display = ('title', 'city', 'state', 'price', 'is_published', 'transfer_to_sold_property')
    list_filter = ('city', 'state', 'is_published')
    search_fields = ('title', 'address', 'city', 'state', 'zipcode')
    actions = ['generate_report']
    list_per_page = 25

    def transfer_to_sold_property(self, obj):
        url = reverse('transfer_listing_to_sold', args=[obj.id])
        return format_html('<a class="button" href="{}">Transfer to Sold</a>', url)
    
    transfer_to_sold_property.short_description = 'Action'


    def generate_report(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        
        # Create the PDF document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        styles['Heading2'].fontSize = 14
        styles['Heading2'].spaceAfter = 12
    
        for listing in queryset:
            # Title
            elements.append(Paragraph(listing.title, styles['Heading1']))
            elements.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 12))

            # Property image
            if listing.photo_main:
                img = Image(listing.photo_main.path, width=6*inch, height=4*inch)
                elements.append(img)
            elements.append(Spacer(1, 12))

            # Property details
            elements.append(Paragraph("Property Details", styles['Heading2']))
            details = [
                f"Title: {listing.title}",
                f"Address: {listing.address}",
                f"Price: {listing.price:,}" if isinstance(listing.price, (int, float)) else f"Price: ${listing.price}"
            ]
            for detail in details:
                elements.append(Paragraph(detail, styles['Normal']))
            elements.append(Spacer(1, 12))

            # Home Open Enquiries
            elements.append(Paragraph("Home Open Enquiries", styles['Heading2']))
            home_open_enquiries = Home_Open_Enquiries.objects.filter(Property=listing.title)
            if home_open_enquiries.exists():
                data = [["Name", "Message", "Contact Date"]]
                for inquiry in home_open_enquiries:
                    data.append([inquiry.name, inquiry.message, inquiry.contact_date.strftime("%Y-%m-%d %H:%M:%S")])
                t = Table(data, colWidths=[2*inch, 4*inch, 1.5*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("No home open enquiries.", styles['Normal']))
            elements.append(Spacer(1, 12))

            # Website Enquiries
            elements.append(Paragraph("Website Enquiries", styles['Heading2']))
            listing_contacts = Contacts.objects.filter(listing=listing.title)
            if listing_contacts.exists():
                data = [["Name", "Message", "Contact Date"]]
                for contact in listing_contacts:
                    data.append([contact.name, contact.message, contact.contact_date.strftime("%Y-%m-%d %H:%M:%S")])
                t = Table(data, colWidths=[2*inch, 4*inch, 1.5*inch])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(t)
            else:
                elements.append(Paragraph("No website enquiries.", styles['Normal']))
            elements.append(Spacer(1, 12))

            # Charts
            home_open_count = home_open_enquiries.count()
            contacts_count = listing_contacts.count()

            # Pie Chart
            elements.append(Paragraph("Enquiries Distribution", styles['Heading2']))
            pie_buffer = BytesIO()
            plt.figure(figsize=(8, 6))
            plt.pie([home_open_count, contacts_count], 
                    labels=["Home Open Enquiries", "Website Enquiries"],
                    autopct='%1.1f%%')
            plt.title("Distribution of Enquiries")
            plt.savefig(pie_buffer, format='png')
            plt.close()
            pie_buffer.seek(0)
            elements.append(Image(pie_buffer, width=4*inch, height=3*inch))
            elements.append(Spacer(1, 12))

            # Bar Graph
            elements.append(Paragraph("Enquiries Comparison", styles['Heading2']))
            bar_buffer = BytesIO()
            plt.figure(figsize=(8, 6))
            plt.bar(['Home Open', 'Website'], [home_open_count, contacts_count])
            plt.title("Comparison of Enquiries")
            plt.savefig(bar_buffer, format='png')
            plt.close()
            bar_buffer.seek(0)
            elements.append(Image(bar_buffer, width=4*inch, height=3*inch))

            # Page break after each listing
            elements.append(PageBreak())

        # Build the PDF
        doc.build(elements)
        return response

    generate_report.short_description = "Generate Report"

    

# Register ListingAdmin in Django Admin
try:
    admin.site.register(Listing, ListingAdmin)
except Exception as e:
    print(f"An error occurred while registering the Listing model with the admin site: {e}")


class ComingSoonAdmin(admin.ModelAdmin):
    list_display = ('address', 'title', 'bedrooms', 'bathrooms', 'carspace', 'area')
    search_fields = ('title', 'address')

class HomeOpenEnquiriesAdmin(admin.ModelAdmin):
    search_fields = ('email', 'name')
    list_display = ('name', 'Property', 'email', 'phone')
    




class HomeOpenAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'has_expired')
    list_filter = ('date',)
    ordering = ('date', 'start_time')  # Order by date and start time in admin panel



admin.site.register(ComingSoon, ComingSoonAdmin)
admin.site.register(Home_Open_Enquiries, HomeOpenEnquiriesAdmin)
admin.site.register(HomeOpen, HomeOpenAdmin)
admin.site.register(UnsubscribedEmail)