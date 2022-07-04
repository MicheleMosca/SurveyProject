# Survey Project

## Setup
Run migrate command to create the site's database:

`python manage.py migrate`

Now create a superuser account:

`python manage.py createsuperuser`

We can now run the server with this command:

`python manage.py runserver 8000`

## Database Image:
![Database Image](db_image.png)

### Database Scheme:
This is the link to [DB Designer Scheme](https://dbdesigner.page.link/egjKR3X2GqZGYSDZ8)

## Features List:
- User login page
- User registration page
- Administration page with link to result pages and the administrator can upload a YAML configuration to manage collections
- A script that interpret the YAML configuration file creating or modifying collections 
- Home page with all Survey_Collection that the user can interact
- Survey_Collection page with all images of the collection showed as a grid and the user can make a rapid answer
- A zoomed view of the Image with the possibly to write a short comment for the answer and move to previous and next Image
- Use of AJAX for form submit without refreshing pages
- An option to show only images without any answer from the user
- Apply transformation to images with the python module Pillow
- A script to decide which transformations must be applied based on a probability argument given by YAML configuration

## How to write YAML Configuration:


### YAML Image Collection File Example:
```
# Definition of a new image collection
collection:
    id: 1                                               # Insert id if you want to add something to an existing collection
    description: "Description of the collection"
    transformations: ['flip(0.5)', 'mirror(0.5)', 'contrast(0.2)']  # Write transformation that can be applied with its probability

    images:
        -   path: "survey/images/image1.jpg"
            name: "image1"                              # name can be omitted, default is the filename without extension
        -   path: "survey/images/image2.jpg"
        -   path: "survey/images/image3.jpg"

    choices:                                            # List new choices for the current image collection
        -   name: "Collection1_Option1"
        -   name: "Collection1_Option2"
        -   name: "Collection1_Option3"
        -   name: "Collection1_Option4"

    users: ['prova1', 'prova2']                         # list new users who will get the access to the collection
```