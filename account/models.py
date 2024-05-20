from django.db import models
import uuid
from datetime import datetime ,date
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/%y/%m/%d')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(User, related_name='liked_posts', default=None)
    no_of_likes = models.IntegerField(default=0)
    type = models.TextField()
    nbrPersonne = models.IntegerField (default=1)


    def __str__(self):
        return f'{self.user.username} - {self.id}'
    
class Reservation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    userPost = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    reservate_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Reservation for {self.post} by {self.user}'


class Stage(Post):
    typeStg= models.IntegerField(default=1)
    societe = models.TextField()
    duree = models.IntegerField(default=1)
    sujet = models.TextField()
    contactInfo = models.TextField()
    specialite = models.TextField()

class Logement (Post):
    localisation= models.TextField()
    description =models.TextField()
    contactInfo =models.TextField()

class Transport (Post):
    depart = models.TextField()
    destination =models.TextField()
    datedepart=models.DateField(default=date.today)
    heureDep= models.IntegerField(default=12)
    nbrSieges = models.IntegerField (default=1)
    contactInfo = models.TextField()

class Recommandation(Post):
    text= models.TextField()

class Event(Post):
    intitule = models.TextField()
    description = models.TextField()
    lieu = models.TextField()
    contactInfo = models.TextField()

class EventClub(Event):
    club=models.TextField()

class EventSocial (Event):
    prix = models.FloatField(default=0.0)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user.username} - {self.post.id}'
    

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ['follower', 'followed_user']
    
    def __str__(self):
        return f'{self.follower.username} follows {self.followed_user.username}'
    
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('Like', 'Like'),
        ('follow', 'Follow'),
        ('comment', 'Comment'),
        ('Reservation', 'Reservation')
    )
    user_post = models.ForeignKey(User, on_delete=models.CASCADE,null=True,  related_name='notifications_received')
    user_notification = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='notifications_sent')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    notificated_at = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user_notification.username} - {self.notification_type}'
