from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Listing, HomeOpen
from .choices import price_choices, bedroom_choices, state_choices
from pages.models import About
from .models import ComingSoon, Home_Open_Enquiries
from django.contrib import messages  
from .utils import generate_qr_code
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from .models import UnsubscribedEmail
from django.shortcuts import redirect
from django.utils import timezone
from datetime import datetime
from django.utils import timezone  # Import timezone utilities
from .models import HomeOpen, Home_Open_Enquiries
from datetime import timedelta
import pytz
from contacts.utils import send_email_and_whatsapp  # Import the function
# listings/views.py
from pages.models import SoldProperty




def listings(request):
    try:
        listings = Listing.objects.order_by('-list_data').filter(is_published=True)
        about_section = About.objects.first()

        paginator = Paginator(listings, 6)
        page = request.GET.get('page')
        paged_listings = paginator.get_page(page)

        context = {
            'listings': paged_listings,
            'about_section': about_section,
        }
        return render(request, 'listings/listings.html', context)
    except Exception as e:
        # Handle the exception, for example, log the error
        print(f"An error occurred in the index view: {e}")
        # Optionally, render an error page or redirect to a specific URL
        return render(request, 'error.html')



def listing(request, slug):
    print(f"Slug received: {slug}")  # Debugging line
    about_section = About.objects.first()

    try:
        listing = get_object_or_404(Listing, slug=slug)
        qr_code_url = listing.qr_code.url if listing.qr_code else None

        # Get the related HomeOpen events for this listing
        now = datetime.now()
        home_opens = listing.home_opens.filter(date__gte=now.date()).order_by('date', 'start_time')
        home_opens = [event for event in home_opens if not event.has_expired()]  # Filter out expired events

        photos = [
            listing.photo_1, listing.photo_2, listing.photo_3, listing.photo_4, listing.photo_5,
            listing.photo_6, listing.photo_7, listing.photo_8, listing.photo_9, listing.photo_10,
            listing.photo_11, listing.photo_12, listing.photo_13, listing.photo_14, listing.photo_15,
            listing.photo_16, listing.photo_17, listing.photo_18
        ]
        photos = [photo for photo in photos if photo]

        context = {
            'listing': listing,
            'about_section': about_section,
            'qr_code_url': qr_code_url,
            'photos': photos,
            'home_opens': home_opens  # Pass non-expired home opens to the template
        }
        return render(request, 'listings/listing.html', context)
    except Exception as e:
        print(f"An error occurred in the listing view: {e}")
        return render(request, 'error.html')



def search(request):
    try:
        queryset_list = Listing.objects.order_by('-list_data')

        # Handle search queries

        context = {
            'state_choices': state_choices,
            'bedroom_choices': bedroom_choices,
            'price_choices': price_choices,
            'listings': queryset_list,
            'values': request.GET,
        }

        return render(request, 'listings/search.html', context)
    except Exception as e:
        print(f"An error occurred in the search view: {e}")
        return render(request, 'error.html')

def coming_soon_view(request):
    coming_soon_items = ComingSoon.objects.all()
    paginator = Paginator(coming_soon_items, 3)  # Display 3 properties per page
    about_section = About.objects.first()
    page_number = request.GET.get('page')
    try:
        paginated_coming_soon_items = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_coming_soon_items = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        paginated_coming_soon_items = paginator.page(paginator.num_pages)

    return render(request, 'listings/coming_soon.html', {'paginated_coming_soon_items': paginated_coming_soon_items, 'about_section': about_section,})




def QR_Enquiry(request):
    # Set the timezone for Perth
    perth_timezone = pytz.timezone('Australia/Perth')
    now = datetime.now(perth_timezone)
    ten_minutes_before = now + timedelta(minutes=10)
    
    # Get the home open event that's starting within the next 10 minutes
    upcoming_event = HomeOpen.objects.filter(
        date=ten_minutes_before.date(),
        start_time__lte=ten_minutes_before.time(),
        end_time__gte=now.time()  # Ensure the event has not ended
    ).order_by('start_time').first()

    property_title = upcoming_event.title if upcoming_event else ''

    if request.method == 'POST':
        try:
            Property = request.POST['Property']
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            message = request.POST['message']
            
            # Save the contact information
            QR_data = Home_Open_Enquiries.objects.create(
                Property=Property,
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            
            # Send notifications
            #send_email_and_whatsapp('Home open', Property, name, email, phone)
            
            messages.success(request, 'Form submitted. Our team will get back to you soon')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return redirect('index')  # Redirect to a suitable page in case of error
    else:
        return render(request, 'Enquiry.html', {'property_title': property_title})






def privacy_policy(request):
    return render(request, 'privacy.html')


@require_POST
def unsubscribe(request, email):
    if email:
        UnsubscribedEmail.objects.get_or_create(email=email)
        # Optionally, you can add a confirmation message here
    return redirect('home')  # Redirect to the home page, change 'home' to your desired URL name



def transfer_listing_to_sold(request, listing_id):
    # Retrieve the Listing instance by ID
    listing = get_object_or_404(Listing, id=listing_id)

    # Create a new SoldProperty instance
    sold_property = SoldProperty()
    
    # Transfer data from Listing to SoldProperty
    sold_property.transfer_from_listing(listing)

    # Optional: Add a success message or redirect to the sold property detail page
    return redirect('sold_property_detail', slug=sold_property.slug)  # Adjust this based on your URL patterns