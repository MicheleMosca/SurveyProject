# Survey Project
![](https://img.shields.io/badge/Python-v3.8-success?logo=Python&logoColor=success)
![](https://img.shields.io/badge/Django-v3.2.9-white?logo=Django&logoColor=white)
![](https://img.shields.io/badge/Pillow-v9.1.1-blue)
 

This site has the purpose of creating surveys on image collections. It allows users, typically dermatologists, to make a diagnosis for a collection of images representing skin diseases   

## Setup
Clone the project from GitHub page:

```
git clone https://github.com/MicheleMosca/SurveyProject.git
cd SurveyProject
```

Run migrate command to create the site's database:

`python manage.py migrate`

Create an Admin account to have access to the Administration Panel:

`python manage.py createsuperuser`

Run the server with this command:

`python manage.py runserver 8000`

The site is now online, you can log in with admin credentials and upload YAML Configuration Files to create new collections

NOTE: The code's documentation can be found to /admin/doc link  

## Database Scheme Image
![Database Image](db_image.png)

### Database Scheme
This is the link to [DB Designer Scheme](https://dbdesigner.page.link/egjKR3X2GqZGYSDZ8)

## Features List
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

## How to write YAML Configuration File
Create a file with .yaml extension and start to define a new collection with the collection tag:

`collection:`

To describe a collection there are six different tags:

- `id: NUMBER`
    With this tag you can specify the id of the collection, is used ONLY if you want to modify an existing collection by adding new images, choices, users or to modify the collection's description

- `description: "DESCRIPTION"`
    Here you can write a short description of the collection

- `transformations: ['TRANSFORMATION(PROBABILITY)', 'TRANSFORMATION(PROBABILITY)']`
    With this tag you can specify a list of transformations that can be applied. Just need to write a valid transformation (for now valid transformation are: 'flip', 'mirror' and 'contrast') and write between round brackets the probability that the transformation can be applied for each user can interact with the collection.

    NOTE: If you want to add new transformations, need to write the Pillow corresponding code in [survey_extras.py](survey/templatetags/survey_extras.py) script and if the transformation contains any parameter need to specify it in [image_collection_loader.py](survey/scripts/image_collection_loader.py) script. (For example: contrast transformation require a factor parameter. It is written in the script)

- `images:`
    Here you can add images to collection by specify the file's path and an optional image name. If the name field is not writen the default name is the filename without extension.
    
    ```
    -   path: "IMAGE_FILE_PATH"
        name: "IMAGE_NAME"
    ```

- `choices:`
    Write all possibly answer option for images of the collection. Users can choose only one option for each image.

    NOTE: At least one option must be written for each collection

    `-   name: "OPTION1"`


- `users: ['USERNAME_USER1','USERNAME_USER2']`
    Specify a list of users that can interact with the collection
    
### YAML Image Collection File Examples
Creation of a new collection:
```
collection:
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

    users: ['user1', 'user2']                         # list new users who will get the access to the collection
```

Modify the collection with id=1 changing the description, adding a new image and a new user:
```
collection:
    id: 1                                               # Insert id only if you want to add something to an existing collection
    description: "Description of the collection modified"

    images:
        -   path: "survey/images/image4.jpg"

    users: ['user3']                         # list new users who will get the access to the collection
```

