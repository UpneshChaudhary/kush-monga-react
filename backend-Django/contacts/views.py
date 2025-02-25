from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contacts, MarketAppraisal, Registered_User
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from twilio.rest import Client
from django.urls import reverse
from twilio.twiml.messaging_response import MessagingResponse
from pages.models import About, TextReview
from datetime import datetime, timedelta
import requests
from django.template.loader import render_to_string
from django.conf import settings
from .models import PropertyOffer

def send_email_and_whatsapp(listing, name, email, phone, message):
    try:
        # Send email
        send_mail(
            'Enquiry from KhushMonga.com',
            f'''
            There has been an Enquiry for {listing}
            Name: {name}
            Email: {email}
            Phone: {phone}
            Message: {message}
            
            Sign into the admin panel for more info
            ''',
            '',
            ['admin@khushmonga.com', 'Khush@baileydevine.com.au', '','upnesh729@gmail.com', 'teammonga@baileydevine.com.au'],
            fail_silently=False
        )

        # Send SMS
        # Assign Twilio Account SID and Auth Token to variables
        
        account_sid = 'ACbf20483358abcb2dfc755d8791045f26'
        auth_token = 'c25f8147d3339e3235522a5eae245df5'

        # Use variables in API URL and key
        sms_api_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
        sms_api_key = f'{account_sid}:{auth_token}'

        sms_message = f' New Enquiry for  {listing} \nFrom: {name}. \nPhone: {phone} \nEmail: {email}. \nMessage: {message}'
        sms_response = requests.post(sms_api_url, auth=(account_sid, auth_token), data={'From': '+17082653249', 'To': '+610411094249', 'Body': sms_message})

        # Initialize Twilio client For WhatsApp Inquiries
        account_sid_ = 'ACbf20483358abcb2dfc755d8791045f26'
        auth_token_ = 'c25f8147d3339e3235522a5eae245df5'
        client = Client(account_sid_, auth_token_)

        # Format the WhatsApp message
        whatsapp_message = f'New Enquiry for  {listing} \nFrom: {name}. \nPhone: {phone} \nEmail: {email}. \nMessage: {message}'

        # Send the WhatsApp message using Twilio
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio-provided WhatsApp number
            body=whatsapp_message,
            to='whatsapp:+61411094249'  # Recipient's WhatsApp number
        )

        print(message.sid)

    except Exception as e:
        print(f'An error occurred while sending email and WhatsApp message: {e}')

def contact(request):
    if request.method == 'POST':
        try:
            listing_id = request.POST['listing_id']
            listing = request.POST['listing']
            name = request.POST['name']
            email = request.POST['email']
            phone = request.POST['phone']
            message = request.POST['message']
            user_id = request.POST['user_id']
            realtor_email = request.POST['realtor_email']
            

            # Save the contact information
            contact = Contacts.objects.create(listing=listing, listing_id=listing_id, name=name, email=email, phone=phone, message=message, user_id=user_id)

            # Send email and WhatsApp message
            send_email_and_whatsapp(listing, name, email, phone, message)

            # Send automatic reply email
            subject = 'Thank you for your enquiry'
            message = f'Thank you for submitting an enquiry, {name}. Khush will be in touch soon. Please feel free to contact her directly on 0411 094 249. Have a nice day.'
            sender_email = settings.EMAIL_HOST_USER
            recipient_email = email
            send_mail(subject, message, sender_email, [recipient_email])



            # Send automatic reply email
            subject = 'Thank you for your enquiry'
            text_message = f"""\
            Thank you for submitting an enquiry, {name}.
            Khush will be in touch soon. Please feel free to contact her directly on 0411 094 249.
            Have a nice day.
            """
            html_message = f"""\
            <p>Thank you for submitting an enquiry, {name}.</p>
            <p>Khush will be in touch soon. Please feel free to contact her directly at 
            <a href="tel:+61411094249">0411 094 249</a>.</p>
            <p>Have a nice day!</p>
            """
            sender_email = settings.EMAIL_HOST_USER
            recipient_email = email
            send_mail(
                subject,
                text_message,
                sender_email,
                [recipient_email],
                html_message=html_message
            )
            messages.success(request, 'Your request has been submitted. Our team will get back to you soon')
            return redirect('/listings')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return HttpResponse('Error processing the request')
    else:
        return HttpResponse('Invalid request')

def register_user(request):
    if request.method == 'POST':
        try:
            # Retrieve form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            purpose = request.POST.get('purpose')
            description = request.POST.get('description')

            # Create a new Registered_User object and save it to the database
            registered_user = Registered_User.objects.create(
                name=name,
                email=email,
                phone=phone,
                purpose=purpose,
                description=description
            )

            # Send email and WhatsApp message
            send_email_and_whatsapp('Register User Form', name, email, phone, f'Purpose: {purpose} \nDescription: {description}')

            # Send automatic reply email
            # subject = 'Thank you for registering with us'
            # message = f'Thank you for registering with us, {name}. Khush will be in touch soon. Please feel free to contact her directly on 0411 094 249. Have a nice day.'
            # sender_email = settings.EMAIL_HOST_USER
            # recipient_email = email
            # send_mail(subject, message, sender_email, [recipient_email])

            messages.success(request, 'Thank you for registering with us. Khush will be in touch with you')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return HttpResponse('Error processing the request')
    else:
        return render(request, 'pages/index.html')

def appraisal(request):
    success_message = None
    about_section = About.objects.first()

    if request.method == 'POST':
        try:
            form_data = request.POST
            MarketAppraisal.objects.create(
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                phone=form_data['phone'],
                email=form_data['email'],
                street_address=form_data['street_address'],
                suburb=form_data['suburb'],
                postcode=form_data['postcode'],
                state=form_data['state'],
                bedrooms=form_data['bedrooms'],
                bathrooms=form_data['bathrooms'],
                cars=form_data['cars'],
                message=form_data['message']
            )

            # Send email and WhatsApp message
            send_email_and_whatsapp('Appraisal Form', form_data['first_name'], form_data['email'], form_data['phone'], f'Message: {form_data["message"]}')


            # # Send automatic reply email
            # subject = 'Thank you for appraisal request'
            # message = f'Thank you for your appraisal request, {first_name}. Khush will be in touch soon. Please feel free to contact her directly on 0411 094 249. Have a nice day.'
            # sender_email = settings.EMAIL_HOST_USER
            # recipient_email = email
            # send_mail(subject, message, sender_email, [recipient_email])


            messages.success(request, 'Your appraisal has been submitted successfully. Thank you!')
            referer_url = request.META.get('HTTP_REFERER', '/')
            return redirect(referer_url)
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return HttpResponse('Error processing the request')
    else:
        return render(request, 'partials/_navbar.html', {'success_message': success_message, 'about_section': about_section})


def submit_review(request):
    if request.method == 'POST':
        stars = request.POST.get('rating')
        review = request.POST.get('newReview')
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Create a new TextReview instance
        review_instance = TextReview.objects.create(
            stars=stars,
            review=review,
            name=name,
            email=email
        )

        #submission_time = datetime.now()

        # Send email, WhatsApp, and SMS
        send_email_and_whatsapp(listing='Review', name=name, email=email, phone='', message=review)
        messages.success(request, '\nThank you for your Review.')
        # You can perform additional actions here if needed

        return redirect('testimonials')

    return render(request, 'pages/testimonial.html')



def property_offer_form(request):
    if request.method == 'POST':
        try:
            form_data = request.POST
            # Create a new PropertyOffer object with form data
            PropertyOffer.objects.create(
                property_address=form_data['property_address'],
                buyer1=form_data['buyer1'],
                email_buyer1=form_data['email_buyer1'],
                buyer2=form_data.get('buyer2', ''),  # Optional field
                email_buyer2=form_data.get('email_buyer2', ''),  # Optional field
                current_address=form_data['current_address'],
                bank_borrowing_from=form_data['bank_borrowing_from'],
                percentage_borrowing_or_cash_offer=form_data['percentage_borrowing_or_cash_offer'],
                current_savings=form_data['current_savings'],
                broker_details=form_data['broker_details'],
                deposit_amount=form_data['deposit_amount'],
                finance_approval_days=form_data['finance_approval_days'],
                settlement_days=form_data['settlement_days'],
                purchase_price=form_data['purchase_price'],
                pre_approval=form_data['pre_approval'],
                contact_number=form_data.get('contact_number', '123-456-7890'),  # New field for contact number with default value
            )

            # Prepare the message for email and WhatsApp
            message = f'''
            Property Address: {form_data['property_address']}
            Buyer 1: {form_data['buyer1']}
            Email Buyer 1: {form_data['email_buyer1']}
            Buyer 2: {form_data.get('buyer2', 'N/A')}
            Email Buyer 2: {form_data.get('email_buyer2', 'N/A')}
            Purchase Price: {form_data['purchase_price']}
            Contact Number: {form_data.get('contact_number', '123-456-7890')}
            '''

            # Send email and WhatsApp message
            send_email_and_whatsapp('Property Offer Form', form_data['buyer1'], form_data['email_buyer1'], form_data.get('contact_number', '123-456-7890'), message)

            # Display success message and redirect to the form page
            messages.success(request, 'Your property offer has been submitted successfully. Thank you!')
            return redirect('index')
        except Exception as e:
            # Display error message if an exception occurs
            messages.error(request, f'An error occurred: {e}')
            # Redirect to the form page to retry
            return redirect('property_offer_form')
    else:
        # Render the form page for GET requests
        return render(request, 'property_offer_form.html')
