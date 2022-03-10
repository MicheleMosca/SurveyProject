from django.db import models
from django.contrib.auth.models import User


class Survey_Collection(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class Survey(models.Model):
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    path = models.CharField(max_length=200)
    transformation = models.CharField(max_length=200)
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.path


class Choice(models.Model):
    name = models.CharField(max_length=200)
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Answer(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    survey_collection = models.ForeignKey(Survey_Collection, on_delete=models.CASCADE, default=1)

    class Meta:
        unique_together = [['image', 'user', 'survey_collection']]
