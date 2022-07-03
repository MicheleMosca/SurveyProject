import base64
import io
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.finders import find
from PIL import Image, ImageOps, ImageEnhance

register = template.Library()


@login_required(login_url='survey:login')
@register.simple_tag
def encode_static_image(path, transformation=''):
    """
    Return a base64 encoded string representation of a static file image and can apply transformations to the image.

    Usage::

        {% encode_static_image path [transformations] %}

    Transformations must be separate by a comma

    Examples::

        {% encode_static_image 'survey/images/ISIC_0463621.jpg' %}
        {% encode_static_image 'survey/images/ISIC_0463621.jpg' 'flip,mirror,contrast(1.11)' %}
        {% encode_static_image 'survey/images/ISIC_0463621.jpg' 'mirror' %}

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
        if 'contrast' in tr:
            enhancer = ImageEnhance.Contrast(img)
            factor = float(tr.split('(')[1].split(')')[0])
            img = enhancer.enhance(factor)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    file_str = base64.b64encode(img_byte_arr).decode('utf-8')

    return f"data:image/{ext};base64,{file_str}"
