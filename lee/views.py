from django.shortcuts import render
from django.http  import HttpResponse
from django.views.generic import ListView
import datetime as dt
from .models import Post

def index(request):
    return render(request, 'index.html')

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-pub_date']
    template_name = 'zj-lee/index.html'
