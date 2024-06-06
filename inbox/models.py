from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timesince import timesince
import uuid

class InboxMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        time_since = timesince(self.created,timezone.now())
        return f"[{self.sender.username} : {time_since} ago]"

    class Meta:
        ordering = ['-created']
        
        
class Conversation(models.Model):
    id = models.CharField(max_length=100, primary_key=True,default=uuid.uuid4,unique=True,editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    lastmessage_created = models.DateTimeField(default=timezone.now)
    is_seen = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-lastmessage_created']

    def __str__(self):
        user_names = ", ".join([user.username for user in self.participants.all()])
        return f"[{user_names}]"
        