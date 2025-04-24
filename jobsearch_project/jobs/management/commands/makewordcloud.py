import os
from collections import Counter

from common.utils import (
    extract_english_nouns,
    extract_korean_nouns,
    get_system_font_path,
    normalize_phrase,
)
from django.core.management.base import BaseCommand
from jobs.models import JobPosting
from wordcloud import WordCloud

from jobsearch_project.settings import BASE_DIR


class Command(BaseCommand):
    help = '채용공고 내용을 기반으로 워드클라우드를 생성합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            help='워드클라우드에 활용될 채용공고 수를 지정합니다. (기본값 500)',
            default=500
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        jobs = JobPosting.objects.exclude(description='nan').exclude(description=None).order_by('-id')[:count]
        self.stdout.write(f'처리할 공고 수: {len(jobs)}건')
        
        self.stdout.write('텍스트 처리 중... (영어/한국어 명사 추출)')
        text = ' '.join([job[0] for job in jobs.values_list('description')])
        korean_nouns = extract_korean_nouns(text)
        english_nouns = extract_english_nouns(text)
        self.stdout.write(f'추출된 명사: 한국어 {len(korean_nouns)}개, 영어 {len(english_nouns)}개')

        combined_nouns = korean_nouns + english_nouns

        self.stdout.write('명사 정규화 처리 중...')
        normalized = [normalize_phrase(p) for p in combined_nouns if normalize_phrase(p)]
        counter = Counter(normalized)

        self.stdout.write('워드클라우드 생성 중...')
        font_path = get_system_font_path()
        wordcloud = WordCloud(
            font_path=font_path,
            background_color='white',
            width=400,
            height=400,
            collocations=False
        ).generate_from_frequencies(counter)
        dir_path = os.path.join(BASE_DIR, 'static/jobs')
        output_path = f'{dir_path}/wordcloud.png'
        wordcloud.to_file(output_path)
        self.stdout.write(self.style.SUCCESS(f'워드클라우드 저장 완료: {output_path}'))
        self.stdout.write(self.style.SUCCESS("작업이 성공적으로 완료되었습니다."))
