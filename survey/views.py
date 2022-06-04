import yaml
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from .models import Survey, Image_Collection, Answer, Choice, Survey_Collection


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


@permission_required('is_superuser')
def adminView(request):
    if request.method == 'POST':
        file = request.FILES['file']
        data = yaml.load(file, Loader=yaml.FullLoader)
        print(data)  # TODO: Collegare lo script di creazione delle collection con questa view

    collection_list = Survey_Collection.objects.all()  # TODO: Creare una pagina di visualizzazione dei risultati

    context = {
        'collection_list': collection_list
    }

    return render(request, 'survey/adminPage.html', context)


@login_required(login_url='survey:login')
def surveyView(request):
    # Write changes on the db
    if request.method == 'POST':
        Answer.objects.update_or_create(
            image_collection_id=request.POST.get('img'),
            user_id=request.user.id,
            defaults={
                'comment': request.POST.get('comment'),
                'choice_id': request.POST.get('answer')
            })
        if request.is_ajax():
            response = {
                'msg': 'Form submitted succesfully!'
            }
            return JsonResponse(response)

    img_id = request.GET.get('img')
    survey_collection_id = request.GET.get('survey_collection_id')
    user_id = request.user.id

    survey_images = Image_Collection.objects.filter(survey_collection_id=survey_collection_id)
    user_answers = Answer.objects.filter(user_id=user_id)
    image = Image_Collection.objects.filter(image_id=img_id,
                                            survey_collection_id=survey_collection_id).first()
    # Check if unvoted checkbox is selected
    show_only_unvoted = False
    if request.GET.get('show_only_unvoted') == 'on':
        show_only_unvoted = True

    images_dict = get_images_dict(survey_images, user_answers, show_only_unvoted)
    images_list = list(images_dict.keys())

    prev_img = None
    next_img = None

    # Check if the current image is an unvoted image, otherwise use the first unvoted image
    if image not in images_list:
        image = images_list[0]

    if images_list.index(image) != 0:
        prev_img = images_list[images_list.index(image) - 1].image_id

    if images_list.index(image) != len(images_list) - 1:
        next_img = images_list[images_list.index(image) + 1].image_id

    choices = Choice.objects.filter(survey_collection_id=survey_collection_id)
    selected_choice = Answer.objects.filter(image_collection_id=image.id,
                                            user_id=user_id).first()
    comment = None
    if selected_choice is not None:
        comment = selected_choice.comment

    context = {
        'image': image,
        'choices': choices,
        'selected_choice': selected_choice,
        'comment': comment,
        'prev': prev_img,
        'next': next_img,
        'show_only_unvoted': show_only_unvoted,
    }
    return render(request, 'survey/survey.html', context)


@login_required(login_url='survey:login')
def homeView(request):
    if request.user.is_superuser:
        return redirect('survey:admin')

    try:
        survey_list = Survey.objects.filter(user_id=request.user.id)
    except (KeyError, Survey.DoesNotExist):
        survey_list = []

    context = {
        'survey_list': survey_list,
    }

    return render(request, 'survey/home.html', context)


def get_images_dict(survey_images, user_answers, show_only_unvoted):
    images_dict = dict()
    for img in survey_images:
        images_dict[img] = None
        for ans in user_answers:
            if ans.image_collection_id == img.id:
                images_dict[img] = ans

    # Remove all voted images from the dict
    img_list = list()
    if show_only_unvoted:
        for img, ans in images_dict.items():
            if ans is not None:
                img_list.append(img)

        for img in img_list:
            images_dict.pop(img)

    return images_dict


@login_required(login_url='survey:login')
def collectionView(request):
    # Write changes on the db
    if request.method == 'POST':
        if request.POST.get('img') is not None:
            Answer.objects.update_or_create(
                image_collection_id=request.POST.get('img'),
                user_id=request.user.id,
                defaults={
                    # 'comment': request.POST.get('comment'), Insert if default comment is needed
                    'choice_id': request.POST.get('answer')
                })
        if request.is_ajax():
            response = {
                'msg': 'Form submitted succesfully!'
            }
            return JsonResponse(response)

    user_id = request.user.id
    survey_collection_id = request.GET.get('survey_collection_id')
    user_answers = Answer.objects.filter(user_id=user_id)
    survey_images = Image_Collection.objects.filter(survey_collection_id=survey_collection_id)

    # Check if unvoted checkbox is selected
    show_only_unvoted = False
    if request.GET.get('show_only_unvoted') == 'on':
        show_only_unvoted = True

    images_dict = get_images_dict(survey_images, user_answers, show_only_unvoted)

    choices = Choice.objects.filter(survey_collection_id=survey_collection_id)

    context = {
        'user_answers': user_answers,
        'survey_images': survey_images,
        'images_dict': images_dict,
        'show_only_unvoted': show_only_unvoted,
        'survey_collection_id': survey_collection_id,
        'choices': choices,
    }
    return render(request, 'survey/collection.html', context)
