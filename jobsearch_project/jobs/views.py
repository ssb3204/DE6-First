from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import JobPosting
# Create your views here.
from django.shortcuts import render
from django.db.models import Q
from .utils import format_description_naturally

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

