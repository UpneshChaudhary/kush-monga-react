from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ListingSitemap  # Import the sitemap classes
from . import views

# Define the sitemaps dictionary
sitemaps = {
    'listings': ListingSitemap,
}

urlpatterns = [
    path('', views.listings, name='listings'),
    path('search/', views.search, name='search'),
    path('coming-soon/', views.coming_soon_view, name='coming_soon'),
    path('HomeOpen_Enquiry/', views.QR_Enquiry, name='HomeOpen_Enquiry'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
    path('transfer/<int:listing_id>/', views.transfer_listing_to_sold, name='transfer_listing_to_sold'),  # Add this line
    path('<slug:slug>/', views.listing, name='listing'),  # This should come last

    # Sitemap URL pattern
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
