from django.db import models

# Create your models here.
class Book(models.Model):
    # JSON 파일의 키(key)와 이름을 맞춰주는 게 좋습니다.
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    description = models.TextField()
    isbn13 = models.CharField(max_length=20, unique=True)
    category_name = models.CharField(max_length=255)
    cover = models.URLField(max_length=500, blank=True, null=True) 
    
    def __str__(self):
        return self.title