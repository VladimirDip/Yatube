from django.shortcuts import render, get_object_or_404
from . models import Group
from posts.models import Post

def group_posts(request,slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})

