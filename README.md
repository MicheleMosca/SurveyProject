# Survey Project

## Setup
`python manage.py runserver 0:8000`

## Upcoming Features:
- [X] User login page
- [X] User registration page
- [ ] Home page
- [ ] Index page with project description
- [ ] Personal User page
- [X] Grid Image view
- [X] Jump to unvoted images

### TODO List:
- [X] Define DB structure
- [X] Write a grid view
- [X] Create a checkbox to visualize only unvoted images
- [ ] Create a new view to serve server with the image in base64
- [ ] Apply Image transformations with pillow and offuscate path in base64
- [ ] Create an upload image script with yaml language
- [ ] Use ajax for the management of the forms on the website
- [ ] Insert a next and previews button near the zoomed image
- [ ] Insert the checkbox to visualize only unvoted images in the zoomed image view
- [ ] sostituire i try/catch con i get

### Database Scheme:
This is the link to [DB Designer Scheme](https://dbdesigner.page.link/egjKR3X2GqZGYSDZ8)

### YAML Image Collection File Example:
```
# Definition of a new image collection
collection:
    id: 1                                               # Insert id if you want to add something to an existing collection
    description: "Description of the collection"

    images:
        -   path: "survey/images/image1.jpg"
            name: "image1"                              # name can be omitted, default is the filename without extension
        -   path: "survey/images/image2.jpg"
            transformation: 'flip'
        -   path: "survey/images/image3.jpg"

    choices:                                            # List new choices for the current image collection
        -   name: "Collection1_Option1"
        -   name: "Collection1_Option2"
        -   name: "Collection1_Option3"
        -   name: "Collection1_Option4"

    users: ['prova1', 'prova2']                         # list new users who will get the access to the collection
```