from django.http import Http404
from django.shortcuts import render,redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Count
from posts.forms import ReplyCreateForm

from .forms import *


def profile(request,username=None):
    
    if username is not None:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
        
    posts = profile.user.posts.all()
    
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')

        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            reply_form = ReplyCreateForm()
            return render(request,'snippets/loop_profile_comments.html',{'comments':comments,'reply_form':reply_form})
        elif 'liked-posts' in request.GET:
            posts = profile.user.likedposts.order_by('-likedpost__created')

        return render(request,'snippets/loop_profile_posts.html',{'posts':posts})
    
    context = {
        "profile": profile,
        "posts": posts
    }
    
    return render(request,'users/profile.html',context)


@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.profile)
    
    if request.method == "POST":
        form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile edited successfully')
            return redirect('profile')
        
        
    if request.path == reverse('profile-onboarding'):
        template = 'users/profile_onboarding.html'
    else:
        template = 'users/profile_edit.html'
        
    return render(request,template,{'form':form})


@login_required
def profile_delete(request):
    
    user = request.user
    
    if request.method == "POST":
        try:
            logout(request)
            user.delete()
            messages.success(request,'Profile deleted successfully')    
            return redirect('/')
        except:
            messages.error(request,'Any error occured')
        return redirect('/')
    
    return render(request,'users/profile_delete.html')