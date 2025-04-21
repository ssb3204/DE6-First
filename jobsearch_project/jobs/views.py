from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import JobPosting
# Create your views here.

from django.shortcuts import render


def index(request):
    return render(request, 'jobs/index.html')

def job_list(request):
    job_list = JobPosting.objects.all().order_by('title')
    paginator = Paginator(job_list, 40)
    page_number = request.GET.get('page') # ?page=2 이런 URL에서 page 번호를 읽음
    page_obj= paginator.get_page(page_number)
    return render(request, 'jobs/job_list.html', {'page_obj': page_obj})

def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    
    # 이전/다음 공고 구하기
    prev_job = JobPosting.objects.filter(pk__lt=pk).order_by('-pk').first()
    next_job = JobPosting.objects.filter(pk__gt=pk).order_by('pk').first()

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'prev_job': prev_job,
        'next_job': next_job
    })

