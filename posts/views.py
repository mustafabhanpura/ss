from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from .models import Post,Author
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def post_list(request):
    if request.user.is_authenticated:
        author = Author.auth_details.get(user = request.user)
        pos=[]
        z =author.following.all()
        pst = Post.published.all()
        for a in z:
            print(a.username)
            for p in pst:
                if str(p.author) == str(a.username):
                    pos.append(p)

        query = request.GET.get('q')
        print(query)
        #if query:
        #    pst = Post.published.filter(title=query)
        context = {
            'pst': pos,
            'z':z
        }
    return render(request, 'posts/post_list.html', context)

def post_list1(request):
    author = Author.auth_details.get(user=request.user)
    z= author.following.all()
    pst = Post.objects.get(author =author)

    print(pst.author)

    return HttpResponse('<h1>Holla</h1>')


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


def post_create(request):
    auth = Author.auth_details.get(user=request.user)
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
    post = Post.published.filter(author = details)
    print(post)
    if details.user in user.following.all():
        follow_1 = False
    else:
        follow_1 =True
    return render(request,'posts/author.html',{'details':details,'follow_1':follow_1,'post':post})

def follow(request,id):
    toggle_user = Author.auth_details.get(id = id)
    if request.user.is_authenticated:
        user_profile,created = Author.auth_details.get_or_create(user=request.user)

        if toggle_user.user in user_profile.following.all():
            user_profile.following.remove(toggle_user.user)
        else:
            user_profile.following.add(toggle_user.user)
    return redirect('/profile_view/'+str(id)+'/')
def my_profile(request):
    auth = Author.auth_details.get(user = request.user)
    post = Post.published.filter(author = auth)

    return render(request,'posts/my_profile.html',{'post':post,'auth':auth})

def followers_list(request,id):
    author = Author.auth_details.get(id=id)
    follower_list = author.user.followed_by.all()
    print(follower_list)
    #if request.user in author.user.followed_by.all():
    #    print(True)

    return render(request,'posts/follower_list.html',{'follower_list':follower_list})
def following_list(request,id):
    author = Author.auth_details.get(id=id)
    foll_list = author.following.all()
    #a= Author.auth_details.filter(user = followers_list)
    print(foll_list)
    #return HttpResponse('<h1>Holla</h1>')
    return render(request,'posts/following_list.html',{'foll_list':foll_list})
