from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import get_object_or_404
from users.models import *
from django.db.models import Q
from .forms import *


@login_required
def inbox(request,conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    
    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
    
    else:
        conversation = None
        
    context = {
        "conversation": conversation,
        "my_conversations": my_conversations
    }
    
    return render(request,'inbox/inbox.html',context)


def search_users(request):
    letters = request.GET.get('search_user')
    
    if request.htmx:
        if len(letters) > 0:
            profiles = Profile.objects.filter(real_name__icontains=letters).exclude(real_name = request.user.profile.real_name)
            users_id = profiles.values_list('user',flat=True)
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(id__in=users_id)
            ).exclude(username = request.user.username)
            
            context = {
                "users": users
            }
            
            return render(request,'inbox/inbox.html',context)
    
        else:
            return HttpResponse("")    
    
    else:
        raise Http404()
    
    
def new_message(request,recipient_id):
    recipient = get_object_or_404(User,id=recipient_id)
    new_message_form = InboxNewMessageForm()
    
    context = {
        "recipient": recipient,
        "new_message_form": new_message_form
    }
    
    return render(request,'inbox/form_newmessage.html',context)
        