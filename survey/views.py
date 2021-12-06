from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def indexView(request):
    return render(request, 'survey/index.html')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'survey/register.html', {'form': form})
