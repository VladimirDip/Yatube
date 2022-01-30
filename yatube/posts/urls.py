from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-news/", views.add_post, name="add_post")

]