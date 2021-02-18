from django.db import models


# Create your models here.
class TherapistProfile(models.Model):
    name = models.CharField(max_length=255)
    methods = models.TextField()
