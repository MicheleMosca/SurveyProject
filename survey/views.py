from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def indexView(request):
    return render(request, 'survey/index.html')


def registerView(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('survey:login')

    return render(request, 'survey/register.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remeber_me')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not remember_me:
                # if the remember me is False it will close the session after the browser is closed
                request.session.set_expiry(0)

            # else browser session will be ad long as the sesison cookie time "SESSION_COOKIE_AGE"
            return redirect('survey:home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    return render(request, 'survey/login.html')


def logoutUser(request):
    logout(request)
    return redirect('survey:login')


@login_required(login_url='survey:login')
def homeView(request):
    return render(request, 'survey/home.html')
