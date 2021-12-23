from django.shortcuts import render
from .models import Post

def index(request):
    latest = Post.objects.order_by("-pub_date")[:10]
    return render(request, "index.html", {"posts": latest})
# Create your views here.
