from django.http import HttpResponse


def IndexView(request):
    return HttpResponse("This is the index page of the survey site.")
