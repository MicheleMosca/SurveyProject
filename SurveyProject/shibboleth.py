from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import HttpResponseRedirect, resolve_url
from django.conf import settings
from django.utils.html import escape
import urllib.request
import requests
from io import BytesIO
from django.core import files
import re
import subprocess


def get_success_url(request):
    url = request.POST.get('next', request.GET.get('next', ''))
    return url or resolve_url(settings.LOGIN_REDIRECT_URL)


def get_remote_image(uid):
    cafile = settings.BASE_DIR + '/shibboleth/tutorato2022.pem'
    image_url = f'https://tutorato.unimore.it/esse3/foto_api/{uid}'

    try:
        response = requests.get(image_url, stream=True, verify=cafile)
        if response.status_code != requests.codes.ok:
            return
        fp = BytesIO()
        fp.write(response.content)
        # A resize could be helpful here
        return fp
    except requests.exceptions.SSLError:
        pass  # TODO: Send e-mail?


def shibboleth_string(field):
    if type(field) is str:
        return field.encode('latin1').decode()
    else:
        return str(field)


def get_shibboleth_list(field):
    s = shibboleth_string(field)
    l = s.split(";")
    l.sort()
    l = [re.sub("{[0-9]}", "", s) for s in l]
    return l


def get_shibboleth_dict(field):
    s = shibboleth_string(field)
    l = s.split(";")
    d = {re.search("{[0-9]}", e).group(0)[1]: re.sub("{[0-9]}", "", e) for e in l}
    return d


# def ignore_ip_in_dos_jail(user, request):
#     for g in user.groups.all():
#         if g.name in teacher_groups:
#             client_ip = get_client_ip(request)
#             jail_name = "http-get-dos"
#             # print("*" * 100)
#             # print(f"{os.getgid()} + {os.getgid()}")
#             # print("*" * 100)
#             cmd = f'fail2ban-client set {jail_name} addignoreip {client_ip}'
#             # print(cmd)
#             subprocess.Popen(cmd, shell=True)
#             return


# def shibboleth_login(request):
#     # if request.session.test_cookie_worked():
#     #     request.session.delete_test_cookie()
#     #     return
#     # else:
#     #     print("Cookies must be enabled")
#
#     meta = request.META
#
#     user, created = User.objects.get_or_create(username=meta["eppn"])
#     if created:
#         user.set_unusable_password()
#
#     if user.email == '' and "mail" in meta:
#         user.email = shibboleth_string(meta["mail"])
#     if user.first_name == '' and "givenName" in meta:
#         user.first_name = shibboleth_string(meta["givenName"]).title()
#     if user.last_name == '' and "sn" in meta:
#         user.last_name = shibboleth_string(meta["sn"]).title()
#
#     user.save()
#
#     if "uid" in meta:
#         uid = shibboleth_string(meta["uid"])
#         user.profile.uid = uid
#         if not user.profile.photo:
#             fp = get_remote_image(uid)
#             if fp:
#                 user.profile.photo.save(uid, files.File(fp), save=False)
#
#     # Sembra che gli "stranieri" non abbiano un affiliation
#     if 'affiliation' in meta.keys() and "student" in shibboleth_string(meta["affiliation"]):  # TODO, check if it works!
#         # Maybe it is better to use get_shibboleth_dict instead of list and take the id '1'
#         user.profile.matricola = get_shibboleth_list(meta["unimorestudmatricola"])[0]
#
#     if "unimorestudcorso" in meta:
#         stud_course_codes = get_shibboleth_dict(meta["unimorestudcorso"])
#
#         stud_course_names = {}
#         if "unimorestuddescrcorso" in meta:
#             stud_course_names = get_shibboleth_dict(meta["unimorestuddescrcorso"])
#
#         for id, code in stud_course_codes.items():
#             family, created = Family.objects.get_or_create(code=code)
#
#             # If the family is news we need to update the name (whenever available)
#             if created and id in stud_course_names:
#                 family.name = stud_course_names[id]
#                 family.save()
#
#             # Old families won't be removed.
#             user.profile.families.add(family)
#
#     user.profile.save()
#
#     user.backend = 'django.contrib.auth.backends.ModelBackend'
#     login(request, user)
#
#     # ignore_ip_in_dos_jail(user, request)
#
#     request.GET.urlencode()
#     return HttpResponseRedirect(get_success_url(request))


def shibboleth_test(request: HttpRequest):
    meta = request.META

    s = '<pre>\n'
    for k, v in meta.items():
        s += k + ': ' + shibboleth_string(v) + ', type: ' + escape(str(type(v))) + '\n'
    s += '</pre>\n'

    return HttpResponse(s)