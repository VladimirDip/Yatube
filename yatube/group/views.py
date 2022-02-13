from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from . models import Group
from posts.models import Post

def group_posts(request,slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "group.html", {"group": group,
                                          "posts": posts,
                                          "page": page,
                                          "paginator": paginator})

