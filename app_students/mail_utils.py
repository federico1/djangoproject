from django.core.mail import send_mail
from django.template.loader import get_template


def send_welcome_mail(form_data):
    ctx = {
        'first_name': form_data['first_name'],
        'last_name': form_data['last_name'],
        'email': form_data['email'],
        'username': form_data['email'],
    }

    html_message = get_template(
        "registration/_mail_signup_confirm.html").render(ctx)

    send_mail(
        subject='Your account at NYC Construction Safety Training, LLC',
        message="Welcome to NYC Construction Safety Training, LLC!",
        html_message=html_message,
        from_email='mail@pdhsafety.com',
        recipient_list=[form_data['email']],
        fail_silently=False
    )
