import threading

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from twilio.rest import Client

from Config import settings
from Config.settings import EMAIL_HOST_USER
from users.models import UserModel, AuthType


@receiver(post_save, sender=UserModel)
def send_verify_code_to_user(sender, instance, created, **kwargs):

    if created:
        code = instance.create_verify_code()

        if instance.auth_type == AuthType.VIA_PHONE:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            client.messages.create(
                body=f"Your instagram verification code is: {code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=instance.phone
            )

        elif instance.auth_type == AuthType.VIA_EMAIL:
            subject = ""
            message = f"Your instagram verification code is: {code}."

            t = threading.Thread(target=send_mail, args=(subject, message, EMAIL_HOST_USER, [instance.email]))
            t.start()
