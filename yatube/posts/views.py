from django.shortcuts import render, get_object_or_404
from .models import Post, Group

def index(request):
    latest = Post.objects.order_by("-pub_date")[:10]
    return render(request, "index.html", {"posts": latest})


