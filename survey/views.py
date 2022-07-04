import yaml
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .models import Survey, Image_Collection, Answer, Choice, Survey_Collection, User, Image_Transformation
from .scripts.image_collection_loader import create_or_modify_collections, errorMsg


def permissionOnSurvey(request):
    """
    Check if user is authorized to interact with this collection
    :param request:
    :return: True if user is authorized, False otherwise
    """
    user_id = request.user.id
    survey_collection_id = request.GET.get('survey_collection_id')
    if not Survey.objects.filter(user_id=user_id, survey_collection_id=survey_collection_id):
        return False
    return True


def indexView(request):
    """
    Display the Index page of the site.

    **Template:**

    :template:`survey/index.html`
    """
    return render(request, 'survey/index.html')


def registerView(request):
    """
    Registration Page for creation of a new :model:`auth.User`

    **Template**

    :template:`survey/register.html`
    """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            response = {
                'msg': 'Account Created'
            }
            return JsonResponse(response)
        else:
            print(form.errors)
            response = {
                'error': f'{form.errors}',
            }
            return JsonResponse(response)

    return render(request, 'survey/register.html')


def loginView(request):
    """
    Login Page

    **Template**

    :template:`survey/login.html`
    """
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
            response = {
                'msg': 'Login Success'
            }
            return JsonResponse(response)
        else:
            response = {
                'error': 'Username or Password is incorrect'
            }
            return JsonResponse(response)

    return render(request, 'survey/login.html')


def logoutUser(request):
    """
    Function doing the logout of user from the site and redirect him to :view:`survey.loginView`
    """
    logout(request)
    return redirect('survey:login')


@permission_required('is_staff')
def adminView(request):
    """
    Display the administration panel where staff member can upload a new yaml configuration and check collection's
    results.

    **Context**

    ``collection_list``
        A list of all :model:`survey.Survey_Collection`.

    **Template**

    :template:`survey/admin_page.html`
    """
    if request.method == 'POST':
        file = request.FILES['file']
        data = yaml.load(file, Loader=yaml.FullLoader)
        print(data)
        return_code = create_or_modify_collections(data)
        if return_code != 0:
            error = {
                'error': errorMsg[return_code]
            }
            response = JsonResponse(error)
            return response

    if request.is_ajax():
        response = {
            'msg': 'Configuration Uploaded! '
        }
        return JsonResponse(response)

    collection_list = Survey_Collection.objects.all()

    context = {
        'collection_list': collection_list
    }

    return render(request, 'survey/admin_page.html', context)


@permission_required('is_staff')
def resultsView(request):
    """
    Display results of :model:`survey.Survey_Collection` given its id.

    **Context**

    ``survey_collection_id``
        The id field of :model:`survey.Survey_Collection`.

    ``img_collection_to_choice_dict``
        A dictionary containing an instance of :model:`survey.Survey_Collection` as key and another dictionary as value,
        this second dictionary contains the name field of :model:`survey.Choice` related to this
        :model:`survey.Survey_Collection` as key and a counter of how many times this choice is selected as value.

    ``user_list``
        A list of all :model:`auth.User` that can interact with this :model:`survey.Survey_Collection`.

    ``choice_list``
        A list of all :model:`survey.Choice` related to this :model:`survey.Survey_Collection`.

    ``users_answer``
        A dictionary containing :model:`survey.Image_Collection` as key and a list as value, this list contains tuples
        formed by (id field of :model:`auth.User`, applied_transformation field of :model:`survey.Image_Transformation`
        , an instance of :model:`survey.Choice` that represent the user's answer for this Image).

    ``transformations``
        Transformations field of :model:`survey.Survey_Collection`.

    **Template**

    :template:`survey/results.html`
    """
    survey_collection_id = request.GET.get('survey_collection_id')
    user_list = [User.objects.filter(id=query[0]).first() for query in
                 Survey.objects.filter(survey_collection_id=survey_collection_id).values_list('user_id')]
    img_collection = [img for img in Image_Collection.objects.filter(survey_collection_id=survey_collection_id)]
    choice = [choice for choice in Choice.objects.filter(survey_collection_id=survey_collection_id)]
    img_collection_to_choice_dict = {i: {c: 0 for c in choice} for i in img_collection}

    for user in user_list:
        for img in img_collection:
            ans_id = Answer.objects.filter(image_collection_id=img.id, user_id=user.id)
            if ans_id:
                (img_collection_to_choice_dict[img])[Choice.objects.filter(id=ans_id.values_list('choice_id')
                                                                           .first()[0]).first()] += 1

    users_answer = {
        img_coll: [
            (user, Image_Transformation.objects.filter(user_id=user.id, image_collection_id=img_coll.id)
             .first().applied_transformation, Answer.objects.filter(user_id=user.id, image_collection_id=img_coll.id)
             .first().choice if Answer.objects.filter(user_id=user.id, image_collection_id=img_coll.id) else '')
            for user in user_list
        ] for img_coll in img_collection
    }

    context = {
        'survey_collection_id': survey_collection_id,
        'img_collection_to_choice_dict': {key: {k2.name: ('%.1f' % (v2 / len(user_list) * 100), v2) for k2, v2
                                                in value.items()} for key, value
                                          in img_collection_to_choice_dict.items()},
        'user_list': user_list,
        'choice_list': list(list(img_collection_to_choice_dict.values())[0].keys()),
        'users_answer': users_answer,
        'transformations': Survey_Collection.objects.filter(id=survey_collection_id).first().transformations,
    }
    return render(request, 'survey/results.html', context)


@login_required(login_url='survey:login')
def surveyView(request):
    """
    Display a single Image (in a zoomed view) of the :model:`survey.Survey_Collection` given its id with a GET
    variable and show its :model:`survey.Choice` to make the user able to make or modify an answer creating a new
    :model:`survey.Answer`.

    **Context**

    ``image_collection``
        An instance of :model:`survey.Image_Collection`, to take information about :model:`survey.Image` and
        :model:`survey.Survey_Collection`

    ``choices``
        An instance of :model:`survey.Choice` filtered by survey_collection_id, to take all possibly choice for this
        :model:`survey.Image` of this :model:`survey.Survey_Collection`

    ``selected_choice``
        An instance of :model:`survey.Answer` to know which :model:`survey.Choice` the user was selected, is None if
        the user hasn't answered yet

    ``comment``
        A String that represent the user's comment, is None if the field is empty

    ``prev``
        The id of the previous :model:`survey.Image`, is None if there isn't a previous image

    ``next``
        The id of the next :model:`survey.Image`, is None if there isn't a next image

    ``show_only_unvoted``
        A boolean variable to know if the user want to see only images that haven't an answer

    ``img_transformation``
        A dictionary with the id of :model:`survey.Image_Image_Collection` as the key and the applied_transformations
        field of :model:`survey.Image_Transformation` as value. It contains a list of transformations that must be
        applied using :tag:`survey_extras-encode_static_image` tag

    **Template**

    :template:`survey/survey.html`
    """
    # check if the user is able to interact with this Survey Collection
    if not permissionOnSurvey(request):
        return HttpResponseForbidden()

    # the user made a new answer, let's write changes on the db
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
                'msg': 'Form submitted successfully!'
            }
            return JsonResponse(response)

    img_id = request.GET.get('img')
    survey_collection_id = request.GET.get('survey_collection_id')
    user_id = request.user.id
    survey_images = Image_Collection.objects.filter(survey_collection_id=survey_collection_id)
    user_answers = Answer.objects.filter(user_id=user_id)
    image_collection = Image_Collection.objects.filter(image_id=img_id,
                                            survey_collection_id=survey_collection_id).first()
    # Check if unvoted checkbox is selected
    show_only_unvoted = False
    if request.GET.get('show_only_unvoted') == 'on':
        show_only_unvoted = True

    # create a dictionary with image id as key and user answer as value, if show_only_unvoted is flagged the dictionary
    # contains only images that haven't an answer
    images_dict = get_images_dict(survey_images, user_answers, show_only_unvoted)
    images_list = list(images_dict.keys())

    prev_img = None
    next_img = None

    # Check if the current image is an unvoted image, otherwise use the first unvoted image
    if image_collection not in images_list:
        image_collection = images_list[0]

    if images_list.index(image_collection) != 0:
        prev_img = images_list[images_list.index(image_collection) - 1].image_id

    if images_list.index(image_collection) != len(images_list) - 1:
        next_img = images_list[images_list.index(image_collection) + 1].image_id

    choices = Choice.objects.filter(survey_collection_id=survey_collection_id)
    selected_choice = Answer.objects.filter(image_collection_id=image_collection.id,
                                            user_id=user_id).first()
    comment = None
    if selected_choice is not None:
        comment = selected_choice.comment

    # create a dictionary with image_transformation_id as the key and the applied_transformations as value
    img_transformation = {
        Image_Transformation.objects.filter(user_id=user_id, image_collection=img).first()
        .image_collection_id: Image_Transformation.objects.filter(user_id=user_id, image_collection=img)
        .first().applied_transformation for img in survey_images
    }

    context = {
        'image_collection': image_collection,
        'choices': choices,
        'selected_choice': selected_choice,
        'comment': comment,
        'prev': prev_img,
        'next': next_img,
        'show_only_unvoted': show_only_unvoted,
        'img_transformation': img_transformation,
    }
    return render(request, 'survey/survey.html', context)


@login_required(login_url='survey:login')
def homeView(request):
    """
    Display the home view of the site, it is accessible only if the user is sign in.
    If the user is a superuser, the site will redirect to :view:`survey.admin` view.

    **Context**

    ``survey_list``
        A lst of all :model:`survey.Survey` connected to the :model:`auth.User`. It is used to extract all
        :model:`survey.Survey_Collection` that the user is allowed to interact

    **Template**

    :template:`survey/home.html`
    """
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
    """
    Get a dict with image id as keys and answer as values for the user given as parameter
    :param survey_images: Image_Collection queryset
    :param user_answers: Answers query set
    :param show_only_unvoted: True to filter only unvoted images
    :return: dict
    """
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
    """
    Display all

    **Context**

    ``user_answers``


    ``survey_images``


    ``images_dict``


    ``show_only_unvoted``


    ``survey_collection_id``


    ``choices``


    ``img_transformation``


    **Template**

    :template:`survey/collection.html`
    """
    if not permissionOnSurvey(request):
        return HttpResponseForbidden()

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

    img_transformation = {
        Image_Transformation.objects.filter(user_id=user_id, image_collection=img).first()
        .image_collection_id: Image_Transformation.objects.filter(user_id=user_id, image_collection=img)
        .first().applied_transformation for img in survey_images
    }

    context = {
        'user_answers': user_answers,
        'survey_images': survey_images,
        'images_dict': images_dict,
        'show_only_unvoted': show_only_unvoted,
        'survey_collection_id': survey_collection_id,
        'choices': choices,
        'img_transformation': img_transformation,
    }
    return render(request, 'survey/collection.html', context)
