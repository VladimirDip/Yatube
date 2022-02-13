from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreatePost
from .models import Post, User


def create_paginator(request, post):
    paginator = Paginator(post, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts_list = Post.objects.select_related(
            "author", "group").filter(
            text__contains=keyword
        )
        print("working")
    else:
        posts_list = Post.objects.order_by("-pub_date").all()

    data_paginator = create_paginator(request, posts_list)
    return render(request, "index.html", {"page": data_paginator[0],
                                          "paginator": data_paginator[1]
                                          }
                  )


@login_required
def new_post(request):
    content = {"title_name": "Новый пост", "btn_name": "Добавить пост"}
    if request.method == "POST":
        form = CreatePost(request.POST)
        if form.is_valid():
            author = request.user
            form.cleaned_data['author'] = author
            date_clean = form.cleaned_data
            post = Post.objects.create(**date_clean)
            return redirect("index")
    else:
        form = CreatePost()
    return render(request, "add_post.html", {"form": form, "content": content})


def profile(request, username):
    user_name = get_object_or_404(User, username=username)
    # print(user_name, "")
    posts = Post.objects.filter(author_id__username=user_name)
    count_posts = posts.count()
    data_paginator = create_paginator(request, posts)
    return render(request, "profile.html", {"page": data_paginator[0],
                                            "count_posts": count_posts,
                                            "paginator": data_paginator[1],
                                            "author": user_name
                                            }
                  )


def post_view(request, username, post_id):
    profile_person = get_object_or_404(User, username=username)
    select_post = get_object_or_404(Post, pk=post_id, author=profile_person.id)
    count_posts = Post.objects.filter(author_id__username=username).count()
    return render(request, "post.html", {"user_post": select_post,
                                         "count_post": count_posts,
                                         "author": profile_person})


def post_edit(request, username, post_id):
    content = {"title_name": "Редактировать запись", "btn_name": "Сохранить"}
    profile_person = get_object_or_404(User, username=username)
    select_post = get_object_or_404(Post, pk=post_id, author=profile_person.id)
    if request.user != profile_person:
        return redirect("post", username=username, post_id=post_id)

    form = CreatePost(request.POST or None, instance=select_post)
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
