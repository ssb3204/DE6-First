from django.shortcuts import render
from . import views
from django.http import HttpResponse
from django.shortcuts import render
from .models import JobPosting
from django.db.models import Q
import csv
import os
from django.shortcuts import render
from django.core.paginator import Paginator


def index(request):
    return render(request, 'jobs/index.html')

from django.db.models import Q
from django.core.paginator import Paginator

from django.db.models import Q
from django.core.paginator import Paginator

from django.db.models import Q
from django.core.paginator import Paginator

def search_page(request):
    query = request.GET.get('q', '')  # 검색어 받기
    filter_by = request.GET.get('filter', 'company')  # 검색할 필드(기본값: company)
    selected_experience = request.GET.getlist('experience')  # 경력 사항 체크박스 필터 받기

    job_postings = JobPosting.objects.all()

    # 검색어로 필터링 (filter_by에 따라 필터링)
    if query:
        if filter_by == 'company':
            job_postings = job_postings.filter(company__icontains=query)
        elif filter_by == 'title':
            job_postings = job_postings.filter(title__icontains=query)
        elif filter_by == 'description':
            job_postings = job_postings.filter(description__icontains=query)
        else:
            # 기본 필터링
            job_postings = job_postings.filter(
                Q(company__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

    # 경력 사항 필터링 (experience_level 필드에서 필터링)
    if selected_experience:
        job_postings = job_postings.filter(experience_level__in=selected_experience)

    # 페이지네이션
    paginator = Paginator(job_postings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/search.html', {
        'page_obj': page_obj,
        'query': query,
        'filter_by': filter_by,
        'selected_experience': selected_experience,
    })




def translate_to_korean(keyword):
    translation_dict = {
        'Java': '자바',
        'Python': '파이썬',
        'C++': 'C++',
        'C#': 'C#',
        'Ruby': 'Ruby',
    }
    return translation_dict.get(keyword, '')

def import_jobs_csv(request):
    # CSV 파일 경로 설정
    file_path = r"C:\Users\ryanp\OneDrive\바탕 화면\final_result.csv"
    
    # 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        return HttpResponse("파일이 존재하지 않습니다.")

    # 기존 데이터 삭제 (초기화)
    JobPosting.objects.all().delete()

    # CSV 파일을 열고 데이터 읽기
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company = row.get('company', row.get('\ufeffcompany', '')).strip()
            title = row.get('title', '').strip()
            link = row.get('link', '').strip()
            description = row.get('description', '').strip()
            source = row.get('source', '').strip()

            # 필수 필드가 없으면 건너뜁니다.
            if not company or not title or not link:
                continue

            # 경력 필터링: description에서 경력 사항에 맞는 값을 추출
            if '경력 1년' in description or '신입' in description:
                experience_level = 'junior'
            elif '경력 2년 이상' in description or '경력 3년 이상' in description:
                experience_level = 'mid'
            elif '경력 5년 이상' in description or '경력 6년 이상' in description or '경력 7년 이상' in description:
                experience_level = 'senior'
            else:
                experience_level = 'junior'  # 기본값 설정, 해당하는 경력이 없으면 신입으로 설정

            # 중복된 링크가 있으면 저장하지 않음
            if not JobPosting.objects.filter(link=link).exists():
                JobPosting.objects.create(
                    company=company,
                    title=title,
                    link=link,
                    description=description,
                    source=source,
                    experience_level=experience_level  # 경력 수준 필드 추가
                )

    return HttpResponse("CSV 파일에서 데이터 가져오기 완료")