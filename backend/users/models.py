from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Create your models here.
def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'profiles/user_{instance.id}/profile.{ext}'

class User(AbstractUser):
    nickname = models.CharField(max_length=30, blank=True, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, default="")  # 소개글

    FAVORITE_COUNTRIES = [
        ('KR', '대한민국'),
        ('JP', '일본'),
        ('CN', '중화권'),
        ('EN', '영미권'),
        ('OTHER', '기타'),
    ]

    FAVORITE_GENRES = [
        ("novel_poem_drama", "소설/시/희곡"),
        ("business", "경제/경영"),
        ("self_help", "자기계발"),
        ("humanities", "인문/철학"),
        ("hobby_practical", "취미/실용"),
        ("comic_ebook", "만화/eBook"),
        ("science", "과학"),
    ]

    favorite_country = models.CharField(max_length=5, choices=FAVORITE_COUNTRIES, null=True, blank=True)
    other_country = models.CharField(max_length=50, null=True, blank=True)
    favorite_genre = models.CharField(max_length=20, choices=FAVORITE_GENRES, null=True, blank=True)
    exp_total = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(
        upload_to=profile_image_path,
        null=True,
        blank=True,
        default='profiles/default_profile.png'
    )
    

class Follow(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following_relations",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follower_relations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["from_user", "to_user"], name="unique_follow"),
        ]