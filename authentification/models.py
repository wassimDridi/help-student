from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
import uuid
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    id_user = models.IntegerField(default=uuid.uuid4)
    phoneNumber = models.IntegerField(blank=True , default=216)
    bio = models.TextField(blank=True , default='')
    utilisateur = models.IntegerField(default=0)
    location = models.CharField(max_length=100, blank=True ,default='')
    profileimg = models.ImageField(upload_to='profile_images/%y/%m/%d', default='blank-profile-picture.png')

    """
    firstName =
        relationship = models.IntegerField(choices=[(0, "None"), (1, "Single"), (2, "In a relationship"), (3, "Married"), (4, "Engaged")], default=0)

    lastName
    phoneNumber
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True) """

    def __str__(self):
        return self.user.username