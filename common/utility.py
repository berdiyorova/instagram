import re
import threading

import phonenumbers
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from twilio.rest import Client

from Config import settings

email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
username_regex = re.compile(r"^[a-zA-z0-9_.-]+$")


def check_email_or_phone(email_or_phone):
    try:
        phone_number = phonenumbers.parse(email_or_phone)
        if phonenumbers.is_valid_number(phone_number):
            email_or_phone = 'phone'
    except:
        if re.fullmatch(email_regex, email_or_phone):
            email_or_phone = "email"

        else:
            data = {
                "success": False,
                "message": "You must enter email or phone number"
            }
            raise ValidationError(data)

    return email_or_phone



def check_user_type(user_input):
    user_type = check_email_or_phone(user_input)
    if not user_type:
        if re.fullmatch(username_regex, user_input):
            user_type = 'username'
        else:
            data = {
                "success": False,
                "message": "You must enter email or phone number or username"
            }
            raise ValidationError(data)

    return user_type


def send_verify_code_to_email(email, code):
    subject = ""
    message = f"Your instagram verification code is: {code}."

    t = threading.Thread(target=send_mail, args=(subject, message, settings.EMAIL_HOST_USER, [email]))
    t.start()


def send_verify_code_to_phone(phone, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=f"Your instagram verification code is: {code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
