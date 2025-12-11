from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'profiles/user_{instance.id}/profile.{ext}'

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True)

    FAVORITE_COUNTRIES = [
        ('KR', '한국'),
        ('JP', '일본'),
        ('ZH', '중화권'),
        ('US', '미국'),
        ('UK', '영국'),
        ('OTHER', '기타'),
    ]

    FAVORITE_GENRES = [
        ('novel', '소설'),
        ('comic', '만화'),
        ('essay', '에세이'),
        ('issue', '시사·이슈'), 
        ('etc', '기타'),
    ]

    favorite_country = models.CharField(max_length=5, choices=FAVORITE_COUNTRIES, null=True, blank=True)
    other_country = models.CharField(max_length=50, null=True, blank=True)
    favorite_genre = models.CharField(max_length=20, choices=FAVORITE_GENRES, null=True, blank=True)

    profile_image = models.ImageField(
        upload_to=profile_image_path,
        null=True,
        blank=True,
        default='profiles/default_profile.png'
    )
    
    