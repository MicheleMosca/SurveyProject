from survey.models import Image
from os import walk
import sys
import yaml


def load_image(path):
    # path = 'static/survey/images/'
    _, _, filenames = next(walk(f'survey/{path}'))

    for f in filenames:
        image = Image(path=f'{path}{f}')
        print(f"{image.path}")


if __name__ == '__main__':
    print("Image Collection Loader\n")

    if len(sys.argv) != 2:
        print(f"Error: incorrect parameters! Usage: {sys.argv[0]} file.yaml")
        exit(1)

    print(f"Load: {sys.argv[1]}")
    file = open(sys.argv[1], "r")
    data = yaml.load(file, Loader=yaml.FullLoader)
    print(data)
