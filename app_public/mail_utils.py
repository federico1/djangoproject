from django.core.mail import send_mail
from django.template.loader import get_template
import requests


def send_contact_alert(form_data):
    try:
  
        message = "Name: {0} /n".format(form_data['name'])
        message += "Email: {0} /n".format(form_data['email'])
        message += "Message: {0} /n".format(form_data['message'])

        html_message = "<p>Name: {0}</p>".format(form_data['name'])
        html_message += "<p>Email: {0}</p>".format(form_data['email'])
        html_message += "<p>Message: {0}</p>".format(form_data['message'])

        send_mail(
            subject='Someone has contacted you at pdhsafety -' + form_data['subject'],
            message=message,
            html_message=html_message,
            from_email='mail@pdhsafety.com',
            #recipient_list=['federico.roca@my.liu.edu', 'mail@pdhsafety.com'],
            recipient_list=['mail@pdhsafety.com'],
            fail_silently=False
        )

        return 1

    except Exception as ex:
        post_firebase(form_data)
        return 0


def post_firebase(form_data):
    try:
        url = 'https://test-api-37a61.firebaseio.com/aus.json'
        x = requests.post(url, json = form_data)

    except Exception as ex:
        return 0