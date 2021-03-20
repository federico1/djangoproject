from django.conf import settings
from django.core.files.base import ContentFile
import base64
import os


def save_base64(image_name, image_data):

    try:
        format, img_str = image_data.split(';base64,')
        directory = os.path.join(settings.MEDIA_ROOT, 'uploads', image_name)

        img_data = base64.b64decode(img_str)
        
        with open(directory, 'wb') as f:
            f.write(img_data)
        
        return os.path.join(settings.MEDIA_URL, 'uploads', image_name)
        
    except:
        return None