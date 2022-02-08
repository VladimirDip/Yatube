from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, User
from .forms import CreatePost
from django.contrib.auth.decorators import login_required


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

    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator})


@login_required
def new_post(request):
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
    return render(request, "add_post.html", {"form": form})

# change it function
def help(request, post):
    paginator = Paginator(post,10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return page, paginator


def profile(request,username):
    user_name = get_object_or_404(User, username=username)
    print(user_name, "")
    posts = Post.objects.filter(author_id__username=user_name)
    count_posts = posts.count()
    m = help(request, posts)
    print(m)
    # print(posts)
    return render(request, "profile.html", {"user_post": m[0],
                                            "count_posts": count_posts,
                                            "paginator": m[1]
                                            }
                  )


def post_view(request, username, post_id):
    profile_person = get_object_or_404(User, username=username)
    select_post = get_object_or_404(Post, pk=post_id, author=profile_person.id)
    print(profile_person, "first")
    print(select_post, "second")
    return render(request, "post.html", {"select_post": select_post})


def post_edit(request, username, post_id):
    return render(request, "add_post.html", {})






