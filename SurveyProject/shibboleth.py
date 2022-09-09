from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.shortcuts import HttpResponseRedirect, resolve_url
from django.conf import settings
from django.utils.html import escape


def get_success_url(request):
    url = request.POST.get('next', request.GET.get('next', ''))
    return url or resolve_url(settings.LOGIN_REDIRECT_URL)


def shibboleth_string(field):
    if type(field) is str:
        return field.encode('latin1').decode()
    else:
        return str(field)


def shibboleth_login(request):
    # if request.session.test_cookie_worked():
    #     request.session.delete_test_cookie()
    #     return
    # else:
    #     print("Cookies must be enabled")

    meta = request.META

    user, created = User.objects.get_or_create(username=meta["eppn"])
    if created:
        user.set_unusable_password()

    if user.email == '' and "mail" in meta:
        user.email = shibboleth_string(meta["mail"])
    if user.first_name == '' and "givenName" in meta:
        user.first_name = shibboleth_string(meta["givenName"]).title()
    if user.last_name == '' and "sn" in meta:
        user.last_name = shibboleth_string(meta["sn"]).title()

    user.save()
    login(request, user)

    request.GET.urlencode()
    return HttpResponseRedirect(get_success_url(request))


def shibboleth_test(request: HttpRequest):
    meta = request.META

    s = '<pre>\n'
    for k, v in meta.items():
        s += k + ': ' + shibboleth_string(v) + ', type: ' + escape(str(type(v))) + '\n'
    s += '</pre>\n'

    return HttpResponse(s)
