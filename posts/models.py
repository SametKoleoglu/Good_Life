from django.db import models
import uuid
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100,null=True)
    url = models.URLField(max_length=400,null=True)
    image = models.URLField(max_length=400)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='posts')
    tags = models.ManyToManyField('Tag')
    likes = models.ManyToManyField(User,related_name='likedposts',through='LikedPost')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True,default=uuid.uuid4,unique=True,editable=False)

    
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering = ['-created_at']
        
    
class LikedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} : {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=20,unique=True)
    image = models.FileField(upload_to='icons/',null=True,blank=True)
    order = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        
        

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User,related_name='likedcomments',through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    
    def __str__(self):
        try:
            return f"{self.author.username} : {self.body[:30]}"
        except:
            return f"No Author : {self.body[:30]}"
        
    class Meta:
        ordering = ['-created']
        
        
class LikedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} : {self.comment.body[:30]}"
        
        
class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='replies')
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User,related_name='likedreplies',through='LikedReply')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    
    def __str__(self):
        try:
            return f"{self.author.username} : {self.body[:30]}"
        except:
            return f"No Author : {self.body[:30]}"
        
    class Meta:
        ordering = ['-created']
        
        
class LikedReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} : {self.reply.body[:30]}"