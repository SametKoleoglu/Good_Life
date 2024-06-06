from django.urls import path
from . import views

urlpatterns = [
    
    #Post Operations
    path("", views.home,name="posts"),
    path("post/create", views.post_create,name="post-create"),
    path("post/delete/<pk>/", views.post_delete,name="post-delete"),
    path("post/edit/<pk>/", views.post_edit,name="post-edit"),
    path("post/<pk>/", views.post_page_view,name="post"),
    path("post/like/<pk>/", views.post_like,name="post-like"),
    path("category/<tag>/", views.home,name="category"),
    
    
    #Comment Operations
    path("comment-sent/<pk>", views.comment_sent,name="comment-sent"),
    path("comment-delete/<pk>/", views.comment_delete,name="comment-delete"),
    path("comment-like/<pk>/", views.comment_like,name="comment-like"),
    path("reply-sent/<pk>", views.reply_sent,name="reply-sent"),
    path("reply-delete/<pk>/", views.reply_delete,name="reply-delete"),
    path("reply-like/<pk>/", views.reply_like,name="reply-like"),
    
]