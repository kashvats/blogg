from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from PIL import Image

# Create your models here.

class post(models.Model):
    heading = models.CharField(max_length=800)
    Image = models.ImageField(upload_to='post')
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.heading

class comment(models.Model):
    post_comment = models.ForeignKey(post,on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default=timezone.now)
    txt = models.CharField(max_length=400)
    def __str__(self):
        return self.txt

class contactus(models.Model):
    name=models.CharField(max_length=20)
    email = models.EmailField(max_length=82)
    message = models.TextField()

    def __str__(self):
        return self.name




