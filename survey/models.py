from django.db import models
from django.contrib.auth.models import User


class Survey_Collection(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.id


class Survey(models.Model):
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    path = models.CharField(max_length=200)
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.path

    class Meta:
        unique_together = [['name', 'path']]


class Image_Collection(models.Model):
    transformation = models.CharField(max_length=200)
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Choice(models.Model):
    name = models.CharField(max_length=200)
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Answer(models.Model):
    image_collection = models.ForeignKey(Image_Collection, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['image_collection', 'user']]
