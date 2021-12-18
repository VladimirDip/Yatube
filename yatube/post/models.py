from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")

class Event(models.Model):
    name = models.CharField(max_length=50)
    start_at = models.DateTimeField("date start", auto_now_add=True)
    description = models.TextField()
    contact = models.EmailField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    location = models.TextField(max_length=400)
# Create your models here.
