from django.shortcuts import render, redirect
from .models import Post
from .forms import CreatePost
from django.contrib.auth.decorators import login_required


def index(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts = Post.objects.select_related("author", "group").filter(text__contains=keyword)
    else:
        posts = Post.objects.order_by("-pub_date")[:10]
    return render(request, "search_text.html", {"posts": posts, "keyword": keyword})

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






