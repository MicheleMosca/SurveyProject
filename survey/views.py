from django.shortcuts import render
from .forms import CreateUserForm


def indexView(request):
    return render(request, 'survey/index.html')


def registerView(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'survey/register.html', {'form': form})
