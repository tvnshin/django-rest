from django.core.mail import send_mail


def send_confirmation_email(email, subject, message):
    send_mail(
        subject,
        message,
        'holder@gmail.com', #change email later
        [email],
        fail_silently=False,
    )