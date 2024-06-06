from django.template import Library
from ..models import * 
from django.db.models import Count


register = Library()


@register.inclusion_tag('includes/sidebar.html')
def sidebar(tag=None,user=None):
    categories = Tag.objects.all()
    top_posts = Post.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')[:5]
    top_comments = Comment.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')[:5]
    context = {
        "categories": categories,
        "tag": tag,
        "top_posts": top_posts,
        "top_comments": top_comments,
        "user": user
    }
    
    return context