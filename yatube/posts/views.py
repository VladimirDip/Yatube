from django.shortcuts import render, redirect
from .models import Post, User
from .forms import CreatePost


# def index(request):
#     latest = Post.objects.order_by("-pub_date")[:10]
#     return render(request, "index.html", {"posts": latest})

# def index(request):
#     author = User.objects.get(username="leo")
#     keyword = "Утро"
#     start_date = datetime.date(1854,7, 7)
#     end_date = datetime.date(1854, 7, 21)
#     posts = Post.objects.filter(text__contains=keyword
#                                 ).filter(author=author
#                                 ).filter(pub_date__range=(start_date, end_date))
#     return render(request, "index.html", {"posts": posts})


def index(request):
    keyword = request.GET.get("q", None)
    if keyword:
        posts = Post.objects.select_related("author", "group").filter(text__contains=keyword)
    else:
        posts = Post.objects.order_by("-pub_date")[:10]
    return render(request, "search_text.html", {"posts": posts, "keyword": keyword})

def add_post(request):
    if request.method == "POST":
        form = CreatePost(request.POST)
        if form.is_valid():
            author = request.user
            form.cleaned_data['author'] = author
            # print(author)
            date_clean = form.cleaned_data
            # print(date_clean)
            post = Post.objects.create(**date_clean)
            return redirect("index")
    else:
        form = CreatePost()
    return render(request, "add_post.html", {"form": form})






