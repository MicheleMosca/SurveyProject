from survey.models import Image
from os import walk

if __name__ == '__main__':
    path = 'static/survey/images/'
    _, _, filenames = next(walk(f'survey/{path}'))

    for f in filenames:
        image = Image(path=f'{path}{f}')
        print(f"{image.path}")
