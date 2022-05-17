import base64
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.finders import find

register = template.Library()


@login_required(login_url='survey:login')
@register.simple_tag
def encode_static(path, encoding='base64', file_type='image'):
    """
        a template tag that returns a encoded string representation of a staticfile
        Usage::
            {% encode_static path [encoding] %}
        Examples::
            <img src="{% encode_static 'path/to/img.png' %}">
    """
    file_path = find(path)
    ext = file_path.split('.')[-1]
    with open(file_path, 'rb') as f:
        file_str = base64.b64encode(f.read()).decode('utf-8')
        f.close()

    return f"data:{file_type}/{ext};{encoding},{file_str}"
