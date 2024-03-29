from django.conf import settings
import random
import string
import shutil
import os
import time
import socket
import hashlib

def uploaded_file(file):
    
    rf = time.strftime("%Y%m%d-%H%M%S")
    file_name = rf + "-" + file.name

    directory = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)

    if handle_uploaded_file(directory, file) <= 0:
        file_name = 0

    return os.path.join(settings.MEDIA_URL, 'uploads', file_name).replace("\\", "/")


def handle_uploaded_file(path, file):
    try:
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            return 1
    except Exception as ex:
        return ex


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception as ex:
        return ""
