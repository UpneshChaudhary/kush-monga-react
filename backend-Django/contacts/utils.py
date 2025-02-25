# contacts/utils.py

from django.core.mail import send_mail
from twilio.rest import Client
import requests
from django.conf import settings

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
            ['admin@khushmonga.com', 'Khush@baileydevine.com.au', '','upnesh729@gmail.com'],
            fail_silently=False
        )

        # Send SMS
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        sms_api_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json'
        sms_api_key = f'{account_sid}:{auth_token}'
        sms_message = f' New Enquiry for  {listing} \nFrom: {name}. \nPhone: {phone} \nEmail: {email}. \nMessage: {message}'
        sms_response = requests.post(sms_api_url, auth=(account_sid, auth_token), data={'From': '+17082653249', 'To': '+610411094249', 'Body': sms_message})

        # Initialize Twilio client for WhatsApp Inquiries
        client = Client(account_sid, auth_token)
        whatsapp_message = f'New Enquiry for  {listing} \nFrom: {name}. \nPhone: {phone} \nEmail: {email}. \nMessage: {message}'
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Twilio-provided WhatsApp number
            body=whatsapp_message,
            to='whatsapp:+61411094249'  # Recipient's WhatsApp number
        )
        print(message.sid)
    except Exception as e:
        print(f'An error occurred while sending email and WhatsApp message: {e}')
