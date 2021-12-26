from django.conf import settings
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template


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




from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    print(result)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
