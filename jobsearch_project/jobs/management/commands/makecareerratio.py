import os

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import pandas as pd
from common.utils import (
    extract_english_nouns,
    extract_korean_nouns,
    get_system_font_path,
)
from django.core.management.base import BaseCommand
from jobs.models import JobPosting

from jobsearch_project.settings import BASE_DIR


class Command(BaseCommand):
    help = '현재 등록된 채용공고의 신입, 경력별 분포의 시각화를 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            help='시각화에 활용될 채용공고 수를 지정합니다. (기본값 500)',
            default=500
        )
    
    def handle(self, *args, **kwargs):
        count = kwargs['count']
        jobs = JobPosting.objects.exclude(description='nan').exclude(description=None).order_by('-id')[:count]
        self.stdout.write(f'처리할 공고 수: {len(jobs)}건')
        
        self.stdout.write('텍스트 처리 중... (영어/한국어 명사 추출)')
        descriptions = ' '.join(jobs.values_list('description', flat=True))
        korean_nouns = extract_korean_nouns(descriptions)
        english_nouns = extract_english_nouns(descriptions)
        self.stdout.write(f'추출된 명사: 한국어 {len(korean_nouns)}개, 영어 {len(english_nouns)}개')

        combined_nouns = korean_nouns + english_nouns
        keywords = ['신입', '경력']
        counts = {keyword: combined_nouns.count(keyword.lower()) for keyword in keywords}
        df = pd.DataFrame([counts])

        font_path = get_system_font_path()
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        plt.figure(figsize=(4, 4))
        plt.pie(df.sum(), labels=keywords, autopct='%1.1f%%', colors=['#3498db', '#e74c3c'], startangle=90)
        plt.axis('equal')
        plt.tight_layout()
        dir_path = os.path.join(BASE_DIR, 'static/jobs')
        output_path = f'{dir_path}/career_ratio.png'
        plt.savefig(output_path, dpi=100, bbox_inches='tight', pad_inches=0.1)
        self.stdout.write(self.style.SUCCESS(f'결과 이미지 저장 완료: {output_path}'))
        self.stdout.write(self.style.SUCCESS("작업이 성공적으로 완료되었습니다."))