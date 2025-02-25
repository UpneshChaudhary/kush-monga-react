from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from contacts.views import submit_review

from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, BlogSitemap, SoldPropertySitemap
from .views import add_to_calendar
from .views import SomeViewSet  # Ensure this is a ViewSet, not a function

# DRF Router
router = DefaultRouter()
#router.register(r'listings', views.ListingViewSet, basename='listing')
router.register(r'sold', views.SoldPropertyViewSet, basename='soldproperties')
router.register(r'blogs', views.BlogViewSet, basename='blog')
router.register(r'about', views.AboutViewSet, basename='about')
router.register(r'feedback-cards', views.FeedbackCardViewSet, basename='feedbackcard')
router.register(r'text-reviews', views.TextReviewViewSet, basename='textreview')
router.register(r'coming-soon', views.ComingSoonViewSet, basename='ComingSoon')
router.register(r'home-opens', views.HomeOpenViewSet, basename='homeopen')
router.register(r'latest-videos', views.LatestVideosViewSet, basename='latest-videos')
router.register(r'appraisals', views.MarketAppraisalViewSet, basename='appraisal')
router.register(r'registered_users', views.RegisteredUserViewSet, basename='registered_users')
router.register(r'listings', views.ListingViewSet, basename='listing')
router.register(r'api/listings/<slug:slug>/', views.ListingDetailView, basename='listing_detail')
router.register(r'api/sold/<slug:slug>/', views.SoldDetailView, basename='sold_detail')
# Register Awards and Certificates APIs
router.register(r'awards', views.AwardViewSet, basename='awards')
router.register(r'certificates', views.CertificateViewSet, basename='certificates')





sitemaps = {
    'static': StaticViewSitemap,
    'blogs': BlogSitemap,
    'sold_properties': SoldPropertySitemap,
    
}

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    #path('api/listings/<slug:slug>/', ListingDetailView.as_view(), name='listing_detail'),
    path('sold/', views.sold_properties, name='sold_properties'),
    #path('sold/<int:sold_property_id>/', views.sold_property_detail, name='sold_property_detail'),
    path('testimonials/', views.testimonial_view, name='testimonials'),
    path('submit_review/', submit_review, name='submit_review'),
    path('feedback_card/<int:pk>/', views.feedback_card_detail, name='feedback_card_detail'),
    path('add_to_calendar/<int:home_open_id>/', add_to_calendar, name='add_to_calendar'),
    path('sold-property/<slug:slug>/', views.sold_property_detail, name='sold_property_detail'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),


    path('api/', include(router.urls)),  # Include all API routes

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
