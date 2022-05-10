from survey.models import Image
from os import walk
import yaml


def load_image(path):
    # path = 'static/survey/images/'
    _, _, filenames = next(walk(f'survey/{path}'))

    for f in filenames:
        image = Image(path=f'{path}{f}')
        print(f"{image.path}")


def run(*args):
    if len(args) != 1:
        print(f"Error: incorrect parameters! file.yaml is needed")
        exit(1)

    print(f"Load: {args[0]}")
    file = open(args[0], "r")
    data = yaml.load(file, Loader=yaml.FullLoader)
    print(data)

    collection = data['collection']
    id = None
    try:
        id = collection['id']
    except KeyError:
        id = None
    if id is not None:
        print(f"Modifico la collection n.{id}")
    else:
        print("Creo una nuova collection")

    print(id)

