from django.contrib.auth.models import User
from django.forms import ModelForm, Textarea
from .models import Post, Comment
from django import forms


class CreatePost(ModelForm):
    class Meta:
        model = Post
        exclude = ['author']
        labels = {
            "text": "Текст",
            "group": "Выберите группу",
            "image": "Фото"
        }


class CreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text": "Текс коментария"
        }
