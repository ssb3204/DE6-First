from django.contrib import admin
from .models import JobPosting

# 모델을 admin에 등록

class QuestionAdmin(admin.ModelAdmin):
  #표시하고 싶은 컬럼
  list_display = ('company','title','source')
  search_fields = ['company','title','source']
  list_filter = ['company']



admin.site.register(JobPosting, QuestionAdmin)