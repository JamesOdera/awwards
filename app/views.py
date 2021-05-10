from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
import datetime as dt
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.forms import modelformset_factory
from django.template.loader import render_to_string
from django.db.models import Q


def index(request):
    posts = Post.objects.all()
    date = dt.date.today()

    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(author__username=query) |
            Q(title__icontains=query)
        )

    context = {
        'posts': posts,
        "date": date,
    }
    return render(request, 'index.html', context)


def nominees(request):
    posts = Post.objects.all()

    context = {
        'posts': posts,
    }
    return render(request, 'nominees.html', context)


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'is_liked': is_liked,
        'post': post,
    }
    if request.is_ajax():
        html = render_to_string(
            'app/comments.html', context, request=request)
        return JsonResponse({'form': html})
    return render(request, 'app/post_detail.html', context)


def like_post(request):
    # post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
        'post': post,
        'total_likes': post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string(
            'app/like_section.html', context, request=request)
        return JsonResponse({'form': html})
    # return HttpResponseRedirect(post.get_absolute_url())


def post_create(request):
    ImageFormset = modelformset_factory(Images, fields=('image',))
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = (request.user)
            post.save()

            for form in formset:
                try:
                    photo = Images(post=post, image=form.cleaned_data['image'])
                    photo.save()

                except Exception as e:
                    break
            return redirect('index')
    else:
        form = PostCreateForm()
        formset = ImageFormset(queryset=Images.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'app/post_create.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse('User is not Active')
            else:
                return HttpResponse('User is None')
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'app/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('user_login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'app/register.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('edit_profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'app/edit_profile.html', context)
