from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
# Create your models here.
