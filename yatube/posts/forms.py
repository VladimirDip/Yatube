from django.contrib.auth.models import User
from django.forms import ModelForm
from . models import Post
from django import forms



class CreatePost(ModelForm):
    class Meta:
        model = Post
        # fields = ['text','group']
        exclude = ['author']


