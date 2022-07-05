from survey.models import Image, Survey_Collection, Image_Collection, User, Survey, Choice, Image_Transformation
import yaml
import random

# Usage:
# python manage.py runscript image_collection_loader --script-args survey/static/survey/collection/new_collection.yaml

errorMsg = {
    1: "Incorrect parameters! file.yaml is needed",
    2: "The new collection doesn't have any choices for the answer!",
    3: "The collection is empty!",
    4: "Choices need a name!"
}


def decision(probability):
    return random.random() < probability


def apply_transformations(image_transformation, transformations, user_id):
    image_transformation.applied_transformation = ''
    for transformation in transformations.split(','):
        probability = float(transformation.split('(')[1].split(')')[0])
        transformation = transformation.split('(')[0]
        if decision(probability):
            # Write here transformation parameter if required
            if transformation == 'contrast':
                # Setting the factor parameter in a (0.5, 1.5) threshold
                factor = "%.2f" % random.uniform(0.5, 1.5)
                transformation += f'({factor})'

            if image_transformation.applied_transformation == '':
                image_transformation.applied_transformation = transformation
            else:
                image_transformation.applied_transformation += ',' + transformation

    print(f"User_id: {user_id} Applied Transformations: {image_transformation.applied_transformation}")
    image_transformation.save()


def add_images(images, collection_object):
    for img in images:
        path = img['path']
        name = img.get('name', (path.split('/')[-1]).split('.')[0])
        transformations = collection_object.transformations

        image_object = Image.objects.get_or_create(
            path=path,
            name=name,
        )[0]
        print(f"path: {image_object.path}  name: {image_object.name}")
        image_collection_object = Image_Collection.objects.get_or_create(image_id=image_object.id,
                                                                         survey_collection_id=collection_object.id)
        image_collection_object[0].save()
        print(f"Image_collection id: {image_collection_object[0].id} "
              f"Image_collection image_id: {image_collection_object[0].image_id} "
              f"Image_collection survey_collection_id: {image_collection_object[0].survey_collection_id}")

        users_id = [user['user_id'] for user in Survey.objects.filter(
            survey_collection_id=collection_object.id).values('user_id')]
        for user_id in users_id:
            image_transformation = Image_Transformation.objects.update_or_create(
                user_id=user_id, image_collection_id=image_collection_object[0].id)[0]
            apply_transformations(image_transformation, transformations, user_id)


def add_users(users, collection_object):
    print(f"Adding new Users: {users}")
    for user in users:
        user_object = User.objects.filter(username=user).first()
        obj, created = Survey.objects.get_or_create(survey_collection_id=collection_object.id, user_id=user_object.id)
        if created:
            print(f"User id: {user_object.id} Username: {user_object.username} added!")
            img_collection_ids = [img_collection['id'] for img_collection in
                                  Image_Collection.objects.filter(survey_collection_id=collection_object.id)
                                  .values('id')]
            for img_collection_id in img_collection_ids:
                image_transformation = Image_Transformation.objects.update_or_create(
                    user_id=user_object.id, image_collection_id=img_collection_id)[0]
                apply_transformations(image_transformation, collection_object.transformations, user_object.id)


def add_choices(choices, collection_object):
    print(f"Choices: {choices}")
    for choice in choices:
        name = choice.get('name')
        if name is None:
            print(f"Error: {errorMsg[4]}")
            return 4

        choice_object = Choice.objects.get_or_create(name=choice['name'], survey_collection_id=collection_object.id)
        print(f"Choice id: {choice_object[0].id} Choice name: {choice_object[0].name} "
              f"Collection id: {choice_object[0].survey_collection_id} added!")


def add_transformations(transformations, collection_object):
    print(f"Transformations: {transformations}")
    transformation_field = transformations[0]
    for transformation in transformations[1:]:
        transformation_field += ',' + transformation

    collection_object.transformations = transformation_field
    collection_object.save()


def create_or_modify_collections(data):
    collection = data.get('collection')
    if collection is None:
        print(f"Error: {errorMsg[3]}")
        return 3

    collection_id = collection.get('id')
    description = collection.get('description', '')
    choices = collection.get('choices')
    transformations = collection.get('transformations')

    if collection_id is not None:
        print(f"Modifico la collection {collection_id}")
        collection_object = Survey_Collection.objects.get(id=collection_id)
        print(f"Collecion id: {collection_object.id} Collection description: {collection_object.description}")

        if description != '':
            collection_object.description = description
            collection_object.save()
            print(f"New description: {collection_object.description}")

    else:
        print("Creo una nuova collection")
        if choices is None:
            print(f"Error: {errorMsg[2]}")
            return 2
        collection_object = Survey_Collection(description=description)
        collection_object.save()
        print(f"Collection id: {collection_object.id}")

    if transformations is not None:
        add_transformations(transformations, collection_object)

    if choices is not None:
        add_choices(choices, collection_object)

    images = collection.get('images')
    if images is not None:
        add_images(images, collection_object)

    users = collection.get('users')
    if users is not None:
        add_users(users, collection_object)

    return 0


def run(*args):
    if len(args) != 1:
        print(f"Error: {errorMsg[1]}")
        return 1

    print(f"Load: {args[0]}")
    file = open(args[0], "r")
    data = yaml.load(file, Loader=yaml.FullLoader)
    print(data)

    return create_or_modify_collections(data)
