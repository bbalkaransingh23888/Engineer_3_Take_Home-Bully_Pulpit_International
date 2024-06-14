from django.db import models

# Create your models here.

class Audience(models.Model):
    file = models.FileField(upload_to='uploads/')
    time_uploaded = models.DateTimeField(auto_now_add=True)