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

def search_page(request):
    query = request.GET.get('q', '')  # 검색어 받기
    filter_by = request.GET.get('filter', 'company')  # 필터링 기준 (기본: 회사)
    selected_experience = request.GET.getlist('experience')  # 경력 사항 체크박스 필터 받기

    job_postings = JobPosting.objects.all()

    # 검색어로 필터링
    if query:
        if query in ['Java', 'Python', 'C++', 'C#', 'Ruby']:
            korean = translate_to_korean(query)
            job_postings = job_postings.filter(
                Q(description__icontains=query) |
                Q(description__icontains=korean)
            )
        else:
            # 일반 검색
            filter_kwargs = {f"{filter_by}__icontains": query}
            job_postings = job_postings.filter(**filter_kwargs)

    # 경력 사항 필터링
    if selected_experience:
        experience_keywords = {
            'junior': '경력 1 |신입',  # '신입' 또는 '경력 1년 이하'를 찾음
            'mid': '경력 2 |경력 3',  # '경력 2년 이상', '경력 3년 이상'을 찾음
            'senior': '경력 5|경력 6|경력 7|경력 8|경력 9',  # '경력 5년 이상'부터 '경력 9년 이상'까지 찾음
        }
        
        # 선택한 경력 사항에 맞는 필터링 적용
        experience_regex = '|'.join([experience_keywords[exp] for exp in selected_experience])
        job_postings = job_postings.filter(description__regex=experience_regex)

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
    file_path = r"C:\Users\ryanp\OneDrive\바탕 화면\final_result.csv"
    if not os.path.exists(file_path):
        return HttpResponse("파일이 존재하지 않습니다.")

    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company = row.get('company', row.get('\ufeffcompany', '')).strip()
            title = row.get('title', '').strip()
            link = row.get('link', '').strip()
            description = row.get('description', '').strip()
            source = row.get('source', '').strip()

            if not company or not title or not link:
                continue

            if not JobPosting.objects.filter(link=link).exists():
                JobPosting.objects.create(
                    company=company,
                    title=title,
                    link=link,
                    description=description,
                    source=source
                )

    return HttpResponse("CSV 파일에서 데이터 가져오기 완료")