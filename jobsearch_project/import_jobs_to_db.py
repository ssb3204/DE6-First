import csv
import os
import django

# Django 프로젝트 설정 등록
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobsearch_project.settings')
django.setup()

from jobs.models import JobPosting

csv_path = os.environ.get('CSV_PATH')

if not csv_path:
    raise ValueError("CSV_PATH 환경변수가 설정되지 않았습니다.")

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        JobPosting.objects.create(
            title=row['title'].strip(),
            company=row['company'].strip(),
            link=row['link'].strip(),
            description=row['description'].strip() if row['description'] else None,
            source=row['source'].strip()
        )
        
print("데이터 삽입 완료")