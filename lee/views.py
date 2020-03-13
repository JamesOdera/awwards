from django.shortcuts import render
from django.http  import HttpResponse
from django.views.generic import ListView, CreateView
import datetime as dt
from .models import Post

def index(request):
    date = dt.date.today()
    images= Image.objects.all()
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'lee/index.html', {"date": date,"images": images},context)

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-pub_date']
    template_name = 'lee/index.html'

class PostCreateView(CreateView):
    model = Post
    fields = [ 'title', 'content', 'cover']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    
