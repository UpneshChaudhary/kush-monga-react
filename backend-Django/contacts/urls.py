from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views 

urlpatterns = [
    path('contact/', csrf_exempt(views.contact), name='contact'),
    #path('send_bulk_email/', csrf_exempt(views.send_bulk_email_view), name='send_bulk_email'),
    path('appraisal/', csrf_exempt(views.appraisal), name='appraisal'),
    path('register/', csrf_exempt(views.register_user), name='register_user'),
    path('property_offer_form/', views.property_offer_form, name='property_offer_form'),
    
]
