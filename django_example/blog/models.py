from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
