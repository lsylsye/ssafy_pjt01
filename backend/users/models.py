from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'profiles/user_{instance.id}/profile.{ext}'

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True, unique=True)
    email = models.EmailField(unique=True)

    FAVORITE_COUNTRIES = [
        ('KR', '한국'),
        ('JP', '일본'),
        ('CN', '중화권'),
        ('EN', '영미권'),
        ('OTHER', '기타'),
    ]

    FAVORITE_GENRES = [
        ("novel_poem_drama", "소설/시/희곡"),
        ("business", "경제/경영"),
        ("self_help", "자기계발"),
        ("humanities", "인문/교양"),
        ("comic_ebook", "만화/eBook"),
        ("science", "과학"),
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
    
    