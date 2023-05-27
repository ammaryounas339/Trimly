from django.db import models

# Create your models here.

class Url(models.Model):
    link = models.URLField(max_length=10000)
    shortened = models.URLField(max_length=10000)