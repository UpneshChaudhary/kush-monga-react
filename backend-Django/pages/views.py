from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from listings.models import Listing, HomeOpen, ComingSoon
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework import status
from listings.models import Listing
from contacts.models import MarketAppraisal, Registered_User
from .serializers import MarketAppraisalSerializer
from .models import SoldProperty
from .serializers import VideoSerializer, RegisteredUserSerializer
from rest_framework.viewsets import ViewSet
from .models import Award, Certificate
from .serializers import AwardSerializer, CertificateSerializer

from .serializers import (
    ListingSerializer,
    SoldPropertySerializer,
    BlogSerializer,
    CertificateSerializer,
    AwardSerializer,
    AboutSerializer,
    FeedbackCardSerializer,
    TextReviewSerializer,
    HomeOpenSerializer,
    ComingSoonSerializer,
    RealtorSerializer,
    GroupedHomeOpenSerializer
)

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import OrderingFilter
from realtors.models import Realtor 
from .models import SoldProperty, Certificate, Award, About
from listings.choices import price_choices, bedroom_choices, state_choices
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blog
from .models import TextReview
from .models import FeedbackCard
from django.http import JsonResponse
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from ics import Calendar, Event
from rest_framework.decorators import api_view

@api_view(['GET'])



def index(request):
    # Fetch the latest 3 published listings with videos
    listings = Listing.objects.order_by('-list_data').filter(is_published=True)[:3]
    video_urls = [listing.video for listing in listings if listing.video]

    # Fetch the latest 3 sold properties
    latest_sold_properties = SoldProperty.objects.order_by('-created_at')[:3]

    about_section = About.objects.first()  # Assuming there's only one about section

    latest_feedback_cards = FeedbackCard.objects.order_by('-created_at')[:3]

    # Fetch upcoming Home Open events, ordered by date and start_time
    now = datetime.now()
    home_open_events = HomeOpen.objects.filter(date__gte=now.date()).order_by('date', 'start_time')
    home_open_events = [event for event in home_open_events if not event.has_expired()]

    # Fetch the latest 3 coming soon properties
    coming_soon_properties = ComingSoon.objects.order_by('-id')[:3]

    context = {
        'listings': listings,
        'latest_sold_properties': latest_sold_properties,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'about_section': about_section,
        'latest_feedback_cards': latest_feedback_cards,
        'home_open_events': home_open_events,
        'video_urls': video_urls,
        'coming_soon_properties': coming_soon_properties,
    }

    return render(request, 'index.html', context)


# def about(request):
#     realtors=Realtor.objects.order_by('-hire_date')

#     mvp_realtors=Realtor.objects.all().filter(is_mvp=True)

#     context= {
#         'realtors':realtors,
#         'mvp_realtors':mvp_realtors
#     }


#     return render(request, 'pages/about.html', context)
def about(request):
    realtors = Realtor.objects.order_by('-hire_date')
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)
    about_section = About.objects.first()
    
    # Fetch the latest 5 published listings
    #listings = Listing.objects.order_by('-list_data').filter(is_published=True)[:5]

    # Fetch all certificates for the carousel
    certificates = Certificate.objects.all()
    all_awards = Award.objects.order_by('-created_at')

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors,
        'certificates': certificates,
        'all_awards': all_awards,
        'about_section': about_section,
    }

    return render(request, 'pages/about.html', context)



# def blog(request):
#     about_section = About.objects.first()

#     context = {'about_section': about_section,}
#     return render(request, 'pages/blog.html')


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    about_section = About.objects.first()
    recent_posts = Blog.objects.all().order_by('-pub_date')[:7]

    context = {
        'blog': blog,
        'about_section': about_section,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'pages/blog_detail.html', context)



# def sold_properties(request):
#     all_sold_properties = SoldProperty.objects.all()
#     context = {'all_sold_properties': all_sold_properties}
#     return render(request, 'sold_properties.html', context)

def sold_properties(request):
    # Fetch all sold properties ordered by created_at in ascending order
    all_sold_properties = SoldProperty.objects.order_by('-created_at')
    about_section = About.objects.first()

    # Paginate the sold properties with 24 items per page
    paginator = Paginator(all_sold_properties, 24)
    page = request.GET.get('page')

    try:
        sold_properties = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        sold_properties = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        sold_properties = paginator.page(paginator.num_pages)

    context = {'sold_properties': sold_properties, 'about_section': about_section}
    return render(request, 'pages/sold.html', context)


def sold_property_detail(request, slug):
    sold_property = get_object_or_404(SoldProperty, slug=slug)
    about_section = About.objects.first()
    
    context = {'sold_property': sold_property, 'about_section': about_section}
    return render(request, 'pages/sold_properties_detail.html', context)

def blog_list(request):
    blog_list = Blog.objects.order_by('-pub_date')
    paginator = Paginator(blog_list, 4)  # Show 4 blogs per page

    recent_posts = Blog.objects.all().order_by('-pub_date')[:7]

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page.
        blogs = paginator.page(paginator.num_pages)

    about_section = About.objects.first()

    context = {
        'blogs': blogs,
        'about_section': about_section,
        'recent_posts': recent_posts,  # Include recent_posts in context
    }

    return render(request, 'pages/blog_list.html', context)




def testimonial_view(request):
    # Fetch text reviews
    text_reviews = TextReview.objects.all().order_by('-uploaded_at')[:99]  # Displaying 16 for initial load
    about_section = About.objects.first()
    # Fetch feedback cards and paginate them, display 6 cards per page
    feedback_cards = FeedbackCard.objects.all()
    paginator = Paginator(feedback_cards, 18)
    page = request.GET.get('page', 1)
    for review in text_reviews:
        review.custom_stars = 5 - review.stars

    try:
        feedback_cards_paginated = paginator.page(page)
    except PageNotAnInteger:
        feedback_cards_paginated = paginator.page(1)
    except EmptyPage:
        feedback_cards_paginated = paginator.page(paginator.num_pages)

    return render(request, 'pages/testimonial.html', {
        'text_reviews': text_reviews,
        'feedback_cards': feedback_cards_paginated,
        'about_section': about_section,
    })


# def submit_review(request):
#     if request.method == 'POST':
#         stars = int(request.POST.get('rating', 1))
#         review_text = request.POST.get('review', '')
        
#         TextReview.objects.create(stars=stars, review=review_text)

#     return redirect('testimonials')




def feedback_card_detail(request, pk):
    feedback_card = get_object_or_404(FeedbackCard, pk=pk)
    about_section = About.objects.first()
    return render(request, 'pages/feedback_card_detail.html', {'feedback_card': feedback_card, 'about_section': about_section})




def add_to_calendar(request, home_open_id):
    # Fetch the home open event from your model
    home_open = HomeOpen.objects.get(id=home_open_id)

    # Create a calendar event
    cal = Calendar()
    event = Event()

    event.name = f"Home Open - {home_open.title}"
    event.begin = datetime.combine(home_open.date, home_open.start_time)
    event.end = datetime.combine(home_open.date, home_open.end_time)
    event.description = f"Visit {home_open.address} for an open house."
    event.location = home_open.address

    cal.events.add(event)

    # Generate .ics file response
    response = HttpResponse(str(cal), content_type="text/calendar")
    response['Content-Disposition'] = f'attachment; filename=home_open_{home_open_id}.ics'
    
    return response




# DRF ViewSets for APIs
# class ListingViewSet(ModelViewSet):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer



# DRF ViewSets for APIs
class ListingViewSet(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'slug'  # Allows retrieving details by slug



class ListingDetailView(ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    lookup_field = 'slug'  # Tells Django to retrieve by 'slug' instead of 'pk'



class SoldPropertyViewSet(ModelViewSet):
    queryset = SoldProperty.objects.all()
    serializer_class = SoldPropertySerializer
    pagination_class = LimitOffsetPagination  # Enables limit and offset
    filter_backends = [OrderingFilter]  # Enables ordering
    ordering_fields = ['created_at']  # Fields allowed for ordering
    ordering = ['-created_at']  # Default ordering (most recent first)
    lookup_field = 'slug'  # Allows retrieving details by slug

class SoldDetailView(ModelViewSet):
    queryset = SoldProperty.objects.all()
    serializer_class = SoldPropertySerializer
    lookup_field = 'slug'  # Allows retrieving details by slug


class BlogPagination(PageNumberPagination):
    page_size = 5  # Adjust as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlogViewSet(ModelViewSet):
    queryset = Blog.objects.all().order_by('-pub_date')
    serializer_class = BlogSerializer
    pagination_class = BlogPagination

class AboutViewSet(ModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer

class FeedbackCardViewSet(ModelViewSet):
    queryset = FeedbackCard.objects.all().order_by('-created_at')
    serializer_class = FeedbackCardSerializer

class TextReviewViewSet(ModelViewSet):
    queryset = TextReview.objects.all().order_by('-uploaded_at')
    serializer_class = TextReviewSerializer

# Add more ViewSets as needed for other models

class ComingSoonViewSet(ModelViewSet):
    queryset = ComingSoon.objects.all()
    serializer_class = ComingSoonSerializer



class HomeOpenViewSet(ModelViewSet):
    serializer_class = GroupedHomeOpenSerializer

    def get_queryset(self):
        now = datetime.now()
        # Filter and order by date and start_time
        home_open_events = HomeOpen.objects.filter(date__gte=now.date()).order_by('date', 'start_time')
        # Exclude expired events
        return [event for event in home_open_events if not event.has_expired()]





class LatestVideosViewSet(ViewSet):
    def list(self, request):
        # Same logic as the APIView
        listings = Listing.objects.filter(video__isnull=False, is_published=True).order_by('-list_data')[:4]
        if listings.count() < 4:
            remaining = 4 - listings.count()
            sold_properties = SoldProperty.objects.filter(video__isnull=False).order_by('-created_at')[:remaining]
        else:
            sold_properties = []

        videos = list(listings) + list(sold_properties)
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)
    

class MarketAppraisalViewSet(ModelViewSet):
    queryset = MarketAppraisal.objects.all().order_by('-created_at')
    serializer_class = MarketAppraisalSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            appraisal = serializer.save()

            # Send email and WhatsApp notification
            send_email_and_whatsapp(
                'Appraisal Form',
                appraisal.first_name,
                appraisal.email,
                appraisal.phone,
                f'Message: {appraisal.message}'
            )

            return Response(
                {"message": "Appraisal submitted successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisteredUserViewSet(ModelViewSet):
    queryset = Registered_User.objects.all()
    serializer_class = RegisteredUserSerializer



# def listing_detail(request, slug):
#     listing = get_object_or_404(Listing, slug=slug)
#     serializer = ListingSerializer(listing)
#     return Response(serializer.data)

# class listing_detail(APIView):
#     def get(self, request, slug):
#         listing = get_object_or_404(Listing, slug=slug)
#         serializer = ListingSerializer(listing)
#         return Response(serializer.data)
# class ListingViewSet(ModelViewSet):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer

# class ListingViewSet(ModelViewSet):
#     queryset = Listing.objects.all()
#     serializer_class = ListingSerializer
#     lookup_field = 'slug'  # Allows retrieving details by slug



class SomeViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Hello from viewset!"})





class AwardViewSet(ModelViewSet):  # ReadOnly to allow only GET requests
    queryset = Award.objects.all().order_by('-created_at')  # Latest first
    serializer_class = AwardSerializer

class CertificateViewSet(ModelViewSet):  # ReadOnly to allow only GET requests
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
