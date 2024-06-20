from django.db import models
from django.utils import timezone


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=50)
    profile_picture = models.CharField(max_length=512)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '<@{}, {}>'.format(self.username, self.email)
