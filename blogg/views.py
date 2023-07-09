from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .form import register, blog_post, contact, cmnt
from .models import post, comment, contactus
import os
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages
import random
from django.core.mail import EmailMessage, send_mail
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# user registration form
#test
def user_register(request):
    if request.method == 'POST':
        ak = register(request.POST)
        if ak.is_valid():
            ak.save()
            return HttpResponseRedirect('/login')
        else:
            messages.error(request, 'Invalid credenitals please fill this form carefully or this username already exist.')
            return HttpResponseRedirect('/register')
    else:
        ak = register()
    return render(request, 'user/register.html', {'bk': ak})


# user log-in form
def user_login(request):
    if request.method == 'POST':
        ak = AuthenticationForm(request=request, data=request.POST)
        if ak.is_valid():
            username = ak.cleaned_data.get('username')
            password = ak.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/dashboard/')
        else:
            messages.error(request, 'Invalid credenitals')
            return HttpResponseRedirect('/login')
    else:

        gm = AuthenticationForm()
        return render(request, 'user/login.html', {'rm': gm})


# user logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


# user dashboard
@login_required(login_url='/login')
def dashboard(request):
    ak = request.user
    pos = post.objects.filter(author=ak)
    return render(request, 'blog/Dashboard.html', {'ak': pos})


# add post by user
@login_required(login_url='/login')
def add(request):
    if request.method == 'POST':
        ak = blog_post(request.POST, request.FILES)
        if ak.is_valid():
            title = ak.cleaned_data.get('heading')
            content = ak.cleaned_data.get('content')
            Image = ak.cleaned_data.get('Image')
            users = request.user
            ready_post = post(heading=title, content=content, author=users, Image=Image)
            ready_post.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        ak = blog_post()
        return render(request, 'blog/post.html', {'add_post': ak})


# edit post by user
@login_required(login_url='/login')
def edit_post(request, id):
    got = post.objects.get(pk=id)
    if len(request.FILES) != 0:
        if len(got.Image) > 0:
            os.remove(got.Image.path)
    if request.method == 'POST':

        ak = blog_post(request.POST, request.FILES, instance=got)
        if request.user.is_authenticated:
            if ak.is_valid():
                title = ak.cleaned_data.get('heading')
                content = ak.cleaned_data.get('content')
                Image = ak.cleaned_data.get('Image')
                users = request.user
                ready_post = post(id=id, heading=title, content=content, author=users, Image=Image)
                ready_post.save()
                return HttpResponseRedirect('/dashboard/')
    else:
        got = post.objects.get(pk=id)
        ak = blog_post(instance=got)
        return render(request, 'blog/editpost.html', {'add_post': ak, 'lot': got})


# delete posts for user
@login_required(login_url='/login')
def del_post(request, id):
    ak = post.objects.get(pk=id).delete()
    return HttpResponseRedirect('/dashboard/')


# post filter by author
def home_post(request, authors):
    cd = authors
    ak = User.objects.get(username=authors)
    bc = post.objects.filter(author=ak).order_by('date')
    return render(request, 'blog/home2.html', {'use': bc})


# landing page for user
def home(request):
    return render(request, 'blog/home.html')


# all post will be shown
def all(request):
    ami = post.objects.all().order_by('-date')
    return render(request, 'blog/allpost.html', {'ap': ami})


# show full post view
def show(request, id):
    py = post.objects.get(pk=id)
    alua = comment.objects.filter(post_comment=py)
    if request.method == 'POST':
        ak = cmnt(request.POST)
        if ak.is_valid():
            name = ak.cleaned_data.get('txt')
            user = request.user
            postt = post.objects.get(pk=id)
            aks = comment(post_comment=postt, user_comment=user, txt=name)
            aks.save()
            return render(request, 'blog/view.html', {'a': py, 'pk': ak, 'kl': alua})

    else:
        ak = cmnt()
        return render(request, 'blog/view.html', {'a': py, 'pk': ak, 'kl': alua})


# full profile will be shown
@login_required(login_url='/login')
def profile(request):
    if request.user.is_authenticated:
        a = request.user
        ami = User.objects.get(username=a)
        return render(request, 'blog/profile.html', {'ap': ami})


@login_required(login_url='/login')
def pass_change(request):
    if request.method == 'POST':
        py = PasswordChangeForm(user=request.user, data=request.POST)
        if py.is_valid():
            py.save()
            return HttpResponseRedirect('/post')
    else:
        py = PasswordChangeForm(user=request.user)
        return render(request, 'user/changepass.html', {'a': py})


def about(request):
    return render(request, 'blog/aboutus.html')


def contra(request):
    if request.method == 'POST':
        ak = contact(request.POST)
        if ak.is_valid():
            lame= request.user
            name = ak.cleaned_data.get('name')
            email = ak.cleaned_data.get('email')
            message = ak.cleaned_data.get('message')
            kam = contactus(name=name, email=email, message=message)
            subject = 'welcome to flogger help'
            kutta = (subject,lame,email)
            pk = send_mail(kutta, message, email, [settings.EMAIL_HOST_USER])
            kam.save()
            return redirect('/post')

    else:
        ak = contact()
        return render(request, 'blog/contactus.html', {'al': ak})


def search(request):
    if request.method == 'GET':
        ak = request.GET['heading']
        see = post.objects.filter(heading__startswith=ak)
        return render(request, 'blog/search.html', {'pk': see, 'gk': ak})
