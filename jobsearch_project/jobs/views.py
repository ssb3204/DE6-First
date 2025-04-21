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
    query = request.GET.get('q', '')
    filter_by = request.GET.get('filter', 'company')

    if query:
        if query in ['Java', 'Python', 'C++', 'C#', 'Ruby']:
            korean = translate_to_korean(query)
            job_list = JobPosting.objects.filter(
                Q(description__icontains=query) |
                Q(description__icontains=korean)
            )
        else:
            # 일반 검색
            filter_kwargs = {f"{filter_by}__icontains": query}
            job_list = JobPosting.objects.filter(**filter_kwargs)
    else:
        job_list = JobPosting.objects.all()

    # 페이지네이션
    paginator = Paginator(job_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/search.html', {
        'page_obj': page_obj,
        'query': query,
        'filter_by': filter_by,
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