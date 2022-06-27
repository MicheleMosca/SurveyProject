import base64
import io
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.finders import find
from PIL import Image, ImageOps

register = template.Library()


@login_required(login_url='survey:login')
@register.simple_tag
def encode_static(path, encoding='base64', file_type='image', transformation=''):
    """
        a template tag that returns a encoded string representation of a staticfile
        Usage::
            {% encode_static path [encoding] %}
        Examples::
            <img src="{% encode_static 'path/to/img.png' %}">
    """
    file_path = find(path)
    ext = file_path.split('.')[-1]
    transformation_list = transformation.split(',')

    img = Image.open(file_path)

    for tr in transformation_list:
        if tr == 'flip':
            img = ImageOps.flip(img)
        if tr == 'mirror':
            img = ImageOps.mirror(img)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    file_str = base64.b64encode(img_byte_arr).decode('utf-8')

    return f"data:{file_type}/{ext};{encoding},{file_str}"
