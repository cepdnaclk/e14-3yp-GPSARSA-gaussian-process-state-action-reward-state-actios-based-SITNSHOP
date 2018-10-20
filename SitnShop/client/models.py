from django.db import models
from django.conf import settings
from django.core.validators import int_list_validator

# Create your models here.


class Client(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    ad1 = models.CharField(max_length=255)
    ad2 = models.CharField(max_length=255)
    ad3 = models.CharField(max_length=255)
    ad4 = models.CharField(max_length=255)
    ad5 = models.CharField(max_length=255)

    timestamp = models.DateTimeField()


    def __str__(self):
        return str(self.user.username)

class Viewer(models.Model):


    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    timestamp = models.DateTimeField()

    def __str__(self):
        return str(self.user.username)
