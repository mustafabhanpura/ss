from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import Post,Author
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def post_list(request):
    pst = Post.published.all()
    query = request.GET.get('q')
    if query:
        pst = Post.published.filter(title=query)
    context = {
        'pst': pst,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, id):
    psts = get_object_or_404(Post, id=id)
    is_liked = False
    if psts.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'psts': psts,
        'is_liked': is_liked,
        'total_likes': psts.total_likes(),
    }
    return render(request, 'posts/post_detail.html', context)


def like_post(request,id):
    # id=request.POST.get('psts_id')
    # id=float(id)
    print(request.user)

    psts = get_object_or_404(Post,id=id)
    is_liked = False
    if psts.likes.filter(id=request.user.id).exists():
        psts.likes.remove(request.user)
        is_liked = False
    else:
        psts.likes.add(request.user)
        is_liked = True
    return HttpResponse('ok this is awesome')
    # return HttpResponseRedirect()

def temp_post(request):
    #print(request.user.username)
    auth = Author.objects.get(user = request.user)
    print(auth.user)
    #details=Post.objects.get(author = auth)
    #print(details)
    return HttpResponse('<h1>Holla</h1>')
def post_create(request):
    auth = Author.objects.get(user=request.user)
    if request.method=='POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            psts = form.save(commit=False)
            psts.author = auth
            psts.save()
            return redirect('/')
    else:
        form = PostCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)
def author(request,id):

    user = Author.auth_details.get(user =request.user)

    details = Author.auth_details.get(id = id)
    temp =[]
    follow=True

    if details.user in user.following.all():
        follow = False
    else:
        follow=True


    return render(request,'posts/author.html',{'details':details,'follow':follow})

def follow(request,id):
    toggle_user = Author.auth_details.get(id = id)
    #toggle_user = get_object_or_404(User,username = request.user)
    #print(toggle_user)
    if request.user:
        user_profile,created = Author.auth_details.get_or_create(user=request.user)
        if toggle_user in user_profile.following.all():
            user_profile.following.remove(toggle_user.user)
            print(user_profile.following.all())
        else:
            user_profile.following.add(toggle_user.user)
    return redirect('/profile_view/'+str(id)+'/')
