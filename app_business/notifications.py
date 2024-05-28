from django.core.mail import send_mail
from django.template.loader import get_template

import logging

logger = logging.getLogger('django')


def mail_welcome_bussiness_user(form_data):
    
    try:
        ctx = {'first_name': form_data['first_name'],
        'last_name': form_data['last_name'],
        'email': form_data['email'],
        'username': form_data['email']}

        html_message = get_template("public/_mail_bussines_signup_confirm.html").render(ctx)

        send_mail(
            subject='Your account at Construction Safety Training, LLC',
            message="Welcome to Construction Safety Training, LLC!",
            html_message=html_message,
            from_email='mail@pdhsafety.com',
            recipient_list=[form_data['email']],
            fail_silently=False)

    except Exception as ex:
        logger.error(ex, exc_info=True)
        return ex
        


