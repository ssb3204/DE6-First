from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import JobPosting
# Create your views here.
from django.shortcuts import render
from django.db.models import Q
from .utils import format_description_naturally
from . import views
from django.http import HttpResponse
import csv
import os



# main 페이지
def index(request):
    return render(request, 'jobs/index.html')


# 채용 공고 리스트 페이지
def job_list(request):
    job_list = JobPosting.objects.all().order_by('title','pk')
    paginator = Paginator(job_list, 40) # 페이지당 40개씩 나누기
    page_number = request.GET.get('page') # ?page=2 이런 URL에서 page 번호를 읽음
    page_obj= paginator.get_page(page_number) # 해당 페이지의 공고 가져오기
    return render(request, 'jobs/job_list.html', {'page_obj': page_obj})

# 채용 공고 상세 페이지
def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    page_number = request.GET.get('page', '1')
    
    # 이전 공고 찾기 (제목-오름차순 기준에서 현재보다 앞선 것)
    prev_job = JobPosting.objects.filter(
        Q(title__lt = job.title) |
        Q(title = job.title, pk__lt = job.pk)
    ).order_by('-title', '-pk').first()
    
    # 다음 공고 찾기 (제목-오름차순 기준에서 현재보다 뒤인 것)
    next_job = JobPosting.objects.filter(
        Q(title__gt = job.title) |
        Q(title = job.title, pk__gt = job.pk)
    ).order_by('title', 'pk').first()
    
    # descripion formatting (잡코리아/링크드인 경우만)
    formatted_description = ""
    if job.source.lower() in ['잡코리아', 'linkedin'] and job.description:
        formatted_description = format_description_naturally(job.description)

    # 
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'prev_job': prev_job,
        'next_job': next_job,
        'formatted_description': formatted_description,
        'page_number': page_number
    })

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
