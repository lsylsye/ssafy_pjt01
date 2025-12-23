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
    

class AIReviewAnalysis(models.Model):
    # ISBN만 있으면 저장 가능 (Book 테이블과 관계없음)
    isbn13 = models.CharField(max_length=13, unique=True)
    
    # 1. AI 
    story_summary = models.TextField(null=True, blank=True)
    summary_reviews = models.JSONField(default=list)
    keywords = models.JSONField(default=list)
    recommend_targets = models.JSONField(default=list)

    # 2. 작가 정보
    author_info = models.TextField(null=True, blank=True)     # 작가 소개
    author_works = models.JSONField(default=list)              # 대표작 리스트
    author_image = models.URLField(null=True, blank=True)      # 작가 사진 URL
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.isbn13} 분석 데이터"