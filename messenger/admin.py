from django.contrib import admin

from .models import Friend , Conversation , Message
# Register your models here.
admin.site.register(Friend)
admin.site.register(Conversation)
admin.site.register(Message)