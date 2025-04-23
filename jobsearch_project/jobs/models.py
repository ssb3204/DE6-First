from django.db import models

class JobPosting(models.Model):
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=50)
    
    # 경력 수준 필드 추가
    EXPERIENCE_LEVEL_CHOICES = [
        ('junior', 'Junior'),    # 신입
        ('mid', 'Mid-Level'),    # 경력 2년 이상
        ('senior', 'Senior'),    # 경력 5년 이상
    ]
    experience_level = models.CharField(
        max_length=6,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='junior'         # 기본값을 신입으로 설정
    )

    def __str__(self):
        return f"{self.title} - {self.company}"

