from django.db import models
from django.contrib.auth.models import User


class Survey_Collection(models.Model):
    """
    Describe a collection of images. It contains an id, a simple description and a list of possibly transformations,
    that can be applied to the set of images by a probability parameter writen inside round brackets
    """
    description = models.CharField(max_length=200)
    transformations = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.id


class Survey(models.Model):
    """
    Connect a :model:`survey.survey_collection` to an :model:`auth.user`. It allow an :model:`auth.User` to interact
    with images of the :model:`survey.survey_collection`
    """
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    """
    Stores images that can be used to create collections. An Image is described by path and name of the image
    """
    path = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.path

    class Meta:
        unique_together = [['name', 'path']]


class Image_Collection(models.Model):
    """
    Connect a single :model:`survey.Image` to a :model:`survey.Survey_Collection`. This allows to create a set of
    images which forms an :model:`survey.Survey_Collection`
    """
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['image', 'survey_collection']]


class Image_Transformation(models.Model):
    """
    Stores the applied transformations list for the :model:`auth.user` to the :model:`survey.Image_Collection`
    """
    applied_transformation = models.CharField(max_length=200)
    image_collection = models.ForeignKey(Image_Collection, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['image_collection', 'user']]


class Choice(models.Model):
    """
    Stores possibly answers for the :model:`survey.Survey_Collection`
    """
    name = models.CharField(max_length=200)
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Answer(models.Model):
    """
    Stores an answer of :model:`auth.User` related to :model:`survey.Image_Collection` and selected from a list of
    possibly answer stored in :model:`survey.Choice`. The user also can write a small comment that justify his choice.
    """
    image_collection = models.ForeignKey(Image_Collection, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['image_collection', 'user']]
