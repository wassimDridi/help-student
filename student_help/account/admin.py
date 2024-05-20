from django.contrib import admin
from .models import Post , Follow , Comment ,Notification
# Register your models here.
from .models import Post , Follow , Comment ,Notification, Event,EventClub,EventSocial,Stage,Transport,Logement,Recommandation
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Notification)

admin.site.register(Event)
admin.site.register(EventClub)
admin.site.register(EventSocial)
admin.site.register(Stage)
admin.site.register(Transport)
admin.site.register(Logement)
admin.site.register(Recommandation)
