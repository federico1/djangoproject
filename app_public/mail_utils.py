from ast import Try
from django.core.mail import send_mail
from django.template.loader import get_template


def send_contact_alert(form_data):
    try:
        message= "Name: " + form_data['name'] + "< br> ";
        message= message + "Message: " + form_data['message'] + "< br> "

        send_mail(
            subject='Someone has contacted you at pdhsafety -' + form_data['subject'],
            message=message,
            html_message=message,
            from_email='mail@pdhsafety.com',
            recipient_list=['shoaib.ijaz8@gmail.com'],
            fail_silently=False
        )

        return 1

    except Exception as ex:
        print(ex)
        return 0

