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
    image = models.ImageField(upload_to='posts/', blank=True, null=True, )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name="Текст коментария")
    created = models.DateTimeField(verbose_name="Дата написания коментария", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", verbose_name="Автор")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ['-created']
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower", verbose_name="Подписчик")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", verbose_name="Подписан")

    class Meta:
        unique_together = ["user", "author"]
        verbose_name = "Подписчика"
        verbose_name_plural = "Подписчики"


