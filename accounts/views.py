from django.shortcuts import render
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from posts.models import Post
from django.urls import reverse
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
############
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# Create your views here.

def user_login(request):
    if request.method=='POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('posts:post_list'))
                else:
                    return HttpResponse("User is inactive")
            else:
                return HttpResponse("User is None")
    else:
        form = UserLoginForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('posts:post_list')

#
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST or None)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             return redirect('post:post_list')
#     else:
#         form=UserRegistrationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'posts/register.html', context)
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('posts/acc_active_email.html', {
                'user':user, 'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            # Sending activation link in terminal
            # user.email_user(subject, message)
            mail_subject = 'Activate your ScrapShut account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            #return HttpResponse('Please confirm your email address to complete the registration.')
            return render(request, 'posts/acc_active_sent.html')
    else:
        form = UserRegistrationForm()
    return render(request,'posts/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return render(request, 'posts/confirmed.html')
    else:
        return HttpResponse('Activation link is invalid!')
