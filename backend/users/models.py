from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'profiles/user_{instance.id}/profile.{ext}'

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)

    profile_image = models.ImageField(
        upload_to=profile_image_path,
        null=True,
        blank=True,
        default='profiles/default_profile.png',
    )