from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_welcome_email(to_email, user_name):
    subject = "Welcome to Fitness Club!"
    
    plain_message = f"Hello {user_name},\n\nWelcome to Fitness Club! We're glad to have you."

    from_email = settings.EMAIL_HOST_USER
    
    send_mail(
        subject,
        plain_message,       
        from_email,
        [to_email],
    )
