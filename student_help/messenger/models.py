from django.db import models
import uuid
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Friend(models.Model):
    user = models.ForeignKey(User, related_name='user_friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_friends', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    last_message = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Conversation between {', '.join([str(participant) for participant in self.participants.all()])}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} - {self.content[:50]}"