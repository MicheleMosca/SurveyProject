from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Survey, Image, Answer, Choice


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
        remember_me = request.POST.get('remember_me')
        print(f"{remember_me}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if remember_me is None:
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
def surveyView(request):
    if request.method == 'POST':
        Answer.objects.update_or_create(
            image_id=request.POST.get('img'),
            user_id=request.user.id,
            survey_collection_id=request.POST.get('survey_collection'),
            defaults={
                'comment': request.POST.get('comment'),
                'choice_id': request.POST.get('answer')
            })

    img_id = request.GET.get('img')
    survey_collection_id = request.GET.get('survey_collection')
    user_id = request.user.id

    image = Image.objects.filter(id=img_id).first()
    choices = Choice.objects.filter(survey_collection_id=survey_collection_id)
    selected_choice = Answer.objects.filter(image_id=img_id,
                                            survey_collection_id=survey_collection_id,
                                            user_id=user_id).first()
    comment = None
    if selected_choice is not None:
        comment = selected_choice.comment

    context = {
        'image': image,
        'choices': choices,
        'selected_choice': selected_choice,
        'comment': comment,
    }
    return render(request, 'survey/survey.html', context)


@login_required(login_url='survey:login')
def homeView(request):
    try:
        survey_list = [Survey.objects.get(user_id=request.user.id)]
    except (KeyError, Survey.DoesNotExist):
        survey_list = []

    context = {
        'survey_list': survey_list,
    }

    return render(request, 'survey/home.html', context)


@login_required(login_url='survey:login')
def resultView(request):
    survey_collection_id = request.GET.get('survey_collection_id')
    user_answers = Answer.objects.filter(user_id=request.user.id)
    survey_images = Image.objects.filter(survey_collection_id=survey_collection_id)

    images_dict = dict()
    for img in survey_images:
        images_dict[img] = None
        for ans in user_answers:
            if ans.image_id == img.id:
                images_dict[img] = ans

    show_only_unanswer = False
    if request.POST.get('show_only_unanswer') == 'on':
        show_only_unanswer = True

    img_list = list()
    if show_only_unanswer:
        for img, ans in images_dict.items():
            if ans is not None:
                img_list.append(img)

        for img in img_list:
            images_dict.pop(img)

    context = {
        'user_answers': user_answers,
        'survey_images': survey_images,
        'images_dict': images_dict,
        'show_only_unanswer': show_only_unanswer,
        'survey_collection_id': survey_collection_id,
    }
    return render(request, 'survey/result.html', context)
