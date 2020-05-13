from django.core import mail
from django.conf.urls.static import settings


def send_email(to, subject, message):
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[to], connection=connection
        ).send()
