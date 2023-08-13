import random
import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from celery import shared_task

from users.models import User


@shared_task()
def send_otp_email(email):
    """Send otp to email and save in base"""
    subject = 'OTP code'
    otp = random.randint(100000, 999999)
    message = f'Your OTP code is {otp}'
    from_email = settings.ADMIN_EMAIL
    send_mail(subject, message, from_email, [email])
    user_obj = get_object_or_404(User, email=email)
    user_obj.otp = otp
    user_obj.otp_date = datetime.datetime.now()
    user_obj.save()
