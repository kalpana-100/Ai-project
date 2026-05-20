# tasks.py

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_welcome_email(email, username, activation_link):
    
    subject = "Welcome to Our Platform"

    context = {
        "username": username,
        "activation_link": activation_link,
    }

    html_content = render_to_string(
        "users/welcome_email.html",
        context
    )

    text_content = f"Hi {username}, Thank you for registering. please click the following link to activate your account: {activation_link}"

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )

    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

    return "Email sent successfully"