from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator


# print(request)
# print(request.method)
# print(request.META)


def home(request,tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag,slug=tag)
    else:
        posts = Post.objects.all()
        
    paginator = Paginator(posts, 3) # Show 3 posts per page
    page = int(request.GET.get('page',1))
    try:  
        posts = paginator.page(page)    
    except:
        return HttpResponse("")
    
    context = {
        "posts": posts,
        "tag": tag,
        "page": page
    }
    
    if request.htmx:
        return render(request, "snippets/loop_home_posts.html",context)
    
    return render(request, "posts/posts_index.html",context)


#POST OPERATIONS

@login_required
def post_create(request):
    form = PostCreateForm()
    
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            source_code = BeautifulSoup(website.text, 'html.parser')

            find_image = source_code.select('meta[content^="https://live.staticflickr.com/"]')
            imaage = find_image[0]['content']
            post.image = imaage
            
            find_title = source_code.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_artist = source_code.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist
            
            post.author = request.user

            post.save()
            form.save_m2m()
    
            return redirect('posts')
    
    context = {
        "form": form
    }
    
    return render(request, "posts/post_create.html",context)


@login_required
def post_delete(request,pk):
    post = get_object_or_404(Post,id=pk,author=request.user)
    
    if request.method == "POST":
        if post:
            post.delete()
            messages.success(request,'Post deleted successfully')
            return redirect('posts')
        else:
            messages.error(request,'Post not found')
            return redirect('post-delete')
    
    context = {
        "post": post
    }

    return render(request,'posts/post_delete.html',context)


@login_required
def post_edit(request,pk):
    post = get_object_or_404(Post,id=pk,author=request.user)
    form = PostEditForm(instance=post)
    
    if request.method == "POST":
        form = PostEditForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post edited successfully')
            return redirect('posts')
    
    context = {
        "form": form,
        "post": post
    }
    
    return render(request,'posts/post_edit.html',context)


def post_page_view(request,pk):
    post = get_object_or_404(Post,id=pk)
    comment_form = CommentCreateForm()
    reply_form = ReplyCreateForm()

    
    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        
        context = {
            "comments": comments,
            "reply_form": reply_form
        }
        
        return render(request,'snippets/loop_postpage_comments.html',context)

            
    context = {
        "post": post,
        "comment_form": comment_form,
        "reply_form": reply_form,
    }
        
    return render(request,'posts/post_page.html',context)
        
    
    context = {
        "post": post,
        "comment_form": comment_form,
        "reply_form": reply_form
    }
    
    return render(request,'posts/post_page.html',context)


def like_toggle(model):
    def inner_func(func):
        def wrapper(request,*args,**kwargs):
            post = get_object_or_404(model,id=kwargs.get('pk'))
            user_exist = post.likes.filter(username = request.user.username).exists()
    
    
            if post.author != request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request,post)
        
        return wrapper
    
    return inner_func


@login_required
@like_toggle(Post)
def post_like(request,post):   
    return render(request,'snippets/likes.html',{'post':post})


@login_required
@like_toggle(Comment)
def comment_like(request,post):
    return render(request,'snippets/likes_comment.html',{'comment':post})



#COMMENT OPERATIONS
@login_required
def comment_sent(request,pk):
    post = get_object_or_404(Post,id=pk)
    reply_form = ReplyCreateForm()
    
    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()
            
        context = {
            "comment": comment,
            "post": post,
            "reply_form": reply_form
        }
            
    return render(request,'snippets/add_comment.html',context)


@login_required
def comment_delete(request,pk):
    post = get_object_or_404(Comment,id=pk,author=request.user)
    
    if request.method == "POST":
            post.delete()
            return redirect('post',post.parent_post.id)

    return render(request,'posts/comment_delete.html',{'comment':post})


@login_required
@like_toggle(Reply)
def reply_like(request,post):
    return render(request,'snippets/likes_reply.html',{'reply':post})



#REPLY OPERATIONS
@login_required
def reply_sent(request,pk):
    comment = get_object_or_404(Comment,id=pk)
    reply_form = ReplyCreateForm()
    
    if request.method == "POST":
        form = ReplyCreateForm(request.POST)
        
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()
            messages.success(request,'Reply sent successfully')
            
    context = {
        "comment": comment,
        "reply_form": reply_form,
        "reply": reply
    }
            
    return render(request,'snippets/add_reply.html',context)


@login_required
def reply_delete(request,pk):
    reply = get_object_or_404(Reply,id=pk,author=request.user)
    
    if request.method == "POST":
            reply.delete()
            messages.success(request,'Reply deleted successfully')
            return redirect('post',reply.parent_comment.parent_post.id)

    return render(request,'posts/reply_delete.html',{'reply':reply})


