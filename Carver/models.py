from django.db import models


# Create your models here.
class Image(models.Model):
    photo = models.ImageField(upload_to=request.session.session_key,blank=False)   # destination to be decided
