from django.db import models
from django.contrib.auth import get_user_model


from group.models import Group

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name="posts",
                              blank=True,
                              null=True)


    class Meta:
        ordering = ['-pub_date']



# Create your models here.
