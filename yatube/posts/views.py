from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.db.models import Count

from .forms import CreatePost, CreateComment
from .models import Post, User, Comment, Follow


def _create_paginator(request, post):
    paginator = Paginator(post, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page, paginator


def _search_text(request):
    keyword = request.GET.get("q", None)
    posts_list = Post.objects.select_related(
        "author", "group").filter(
        text__contains=keyword
    ).prefetch_related("comments")
    data_paginator = _create_paginator(request, posts_list)
    return data_paginator

@cache_page(20, key_prefix="index_page")
def index(request):
    if request.GET.get("q") is None:
        posts_list = Post.objects.order_by("-pub_date")\
            .all()\
            .select_related("author", "group", )\
            .prefetch_related("comments",)
        data_paginator = _create_paginator(request, posts_list)
    else:
        data_paginator = _search_text(request)

    return render(request, "index.html", {"page": data_paginator[0],
                                          "paginator": data_paginator[1],
                                          "title": "Последние обновления",
                                          "description": "Последние обновления на сайте",
                                          "changing_it": "index"})


@login_required
def new_post(request):
    content = {"title_name": "Новый пост", "btn_name": "Добавить пост"}
    if request.method == "POST":
        form = CreatePost(request.POST, files=request.FILES or None)
        if form.is_valid():
            author = request.user
            form.cleaned_data['author'] = author
            date_clean = form.cleaned_data
            post = Post.objects.create(**date_clean)
            messages.success(request, "Пост добавлен")
            return redirect("index")
    else:
        form = CreatePost()
    return render(request, "add_post.html", {"form": form, "content": content})


def profile(request, username):
    user_name = get_object_or_404(User, username=username)
    print(user_name.following.all())
    posts = Post.objects.filter(author_id__username=user_name)\
        .select_related("author", "group")\
        .prefetch_related("comments")
    data_paginator = _create_paginator(request, posts)
    return render(request, "profile.html", {"page": data_paginator[0],
                                            "paginator": data_paginator[1],
                                            "author": user_name})


def post_view(request, username, post_id):
    profile_person = get_object_or_404(User, username=username)
    print(type(profile_person))
    select_post = get_object_or_404(Post, pk=post_id, author=profile_person.id)
    # comments = select_post.comments.all()
    comments = list(Comment.objects.filter(post_id=post_id).select_related("author", "post"))

    return render(request, "post.html", {"user_post": select_post,
                                         "author": profile_person,
                                         "comments": comments})


def post_edit(request, username, post_id):
    content = {"title_name": "Редактировать запись", "btn_name": "Сохранить"}
    profile_person = get_object_or_404(User, username=username)
    select_post = get_object_or_404(Post, pk=post_id, author=profile_person.id)
    if request.user != profile_person:
        return redirect("post", username=username, post_id=post_id)

    form = CreatePost(request.POST or None,
                      instance=select_post,
                      files=request.FILES or None)
    if form.is_valid():
        form.save()
        print("Post can editable")
        return redirect("post", username=username, post_id=post_id)

    return render(request, "add_post.html", {"form": form,
                                             "selected_post": select_post,
                                             "content": content})


def page_not_found(request, exeption):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    profile_person = get_object_or_404(User, username=username)
    select_post = get_object_or_404(Post, pk=post_id, author=profile_person)
    if request.method == "POST":
        form = CreateComment(request.POST)
        print(form)
        if form.is_valid():
            author = request.user
            form.cleaned_data["post"] = select_post
            form.cleaned_data["author"] = author
            data_clean = form.cleaned_data
            comment = Comment.objects.create(**data_clean)
            messages.success(request, "Коммент поставлен")
            return redirect("post", username=username, post_id=post_id)
    else:
        form = CreateComment()
    return render(request, "comments.html", {"form": form})


@login_required
def follow_index(request):
    my_follow = Post.objects.filter(author__following__user=request.user)\
        .select_related("author", "group")\
        .prefetch_related("comments")

    data_paginator = _create_paginator(request, my_follow)

    return render(request, "index.html", {"page": data_paginator[0],
                                           "paginator": data_paginator[1],
                                           "title": "Подписки",
                                           "description": "Последние обновления твоих людей",
                                           "changing_it": "follow"})

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(author=author, user=request.user)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    unfollow = Follow.objects.get(author=username, user=request.user.id)
    unfollow.delete()
    return redirect('profile', username=username)