from survey.models import Image, Survey_Collection, Image_Collection, User, Survey, Choice
import yaml


def image_loader(images, collection_object):
    for img in images:
        path = img['path']
        try:
            name = img['name']
        except KeyError:
            name = (path.split('/')[-1]).split('.')[0]

        try:
            transformation = img['transformation']
        except KeyError:
            transformation = ''

        image_object = Image.objects.get_or_create(
            path=path,
            name=name,
        )[0]
        print(f"path: {image_object.path}  name: {image_object.name}")
        image_collection_object = Image_Collection.objects.get_or_create(image_id=image_object.id,
                                                                         survey_collection_id=collection_object.id)
        image_collection_object[0].transformation = transformation
        image_collection_object[0].save()
        print(f"Image_collection id: {image_collection_object[0].id} "
              f"Image_collection image_id: {image_collection_object[0].image_id} "
              f"Image_collection survey_collection_id: {image_collection_object[0].survey_collection_id} "
              f"Image_collection transformation: {image_collection_object[0].transformation}")


def add_users(users, collection_object):
    print(f"Adding new Users: {users}")
    for user in users:
        user_object = User.objects.filter(username=user).first()
        Survey.objects.get_or_create(survey_collection_id=collection_object.id, user_id=user_object.id)
        print(f"User id: {user_object.id} Username: {user_object.username} added!")


def add_choices(choices, collection_object):
    print(f"Choices: {choices}")
    for choice in choices:
        try:
            choice_object = Choice.objects.get_or_create(name=choice['name'], survey_collection_id=collection_object.id)
            print(f"Choice id: {choice_object[0].id} Choice name: {choice_object[0].name} "
                  f"Collection id: {choice_object[0].survey_collection_id} added!")
        except KeyError:
            print("Errore: Choices need a name!")
            exit(4)


def run(*args):
    if len(args) != 1:
        print(f"Error: incorrect parameters! file.yaml is needed")
        exit(1)

    print(f"Load: {args[0]}")
    file = open(args[0], "r")
    data = yaml.load(file, Loader=yaml.FullLoader)
    print(data)

    try:
        collection = data['collection']
        if collection is None:
            print("Error: The collection is empty!")
            exit(5)

        try:
            collection_id = collection['id']
        except KeyError:
            collection_id = None

        try:
            description = collection['description']
        except KeyError:
            description = ''

        try:
            choices = collection['choices']
        except KeyError:
            choices = None
            if collection_id is None:
                print("Errore: The new collection doesn't have any choices for the answer!")
                exit(2)

        if collection_id is not None:
            print(f"Aggiungo le seguenti immagini alla collection {collection_id}")
            collection_object = Survey_Collection.objects.get(id=collection_id)
            print(f"Collecion id: {collection_object.id} Collection description: {collection_object.description}")

            if description != '':
                collection_object.description = description
                collection_object.save()
                print(f"New description: {collection_object.description}")

        else:
            print("Creo una nuova collection")
            collection_object = Survey_Collection(description=description)
            collection_object.save()
            print(f"Collection id: {collection_object.id}")

        if choices is not None:
            add_choices(choices, collection_object)

        try:
            images = collection['images']
            image_loader(images, collection_object)
        except KeyError:
            pass

        try:
            users = collection['users']
            add_users(users, collection_object)
        except KeyError:
            pass

    except KeyError:
        print("Error: No collection found!")
        exit(3)
