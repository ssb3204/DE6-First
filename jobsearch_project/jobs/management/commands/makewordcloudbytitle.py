import os
from collections import Counter

import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from common.utils import (
    extract_english_nouns,
    extract_korean_nouns,
    get_system_font_path,
    normalize_phrase2,
    format_years
)
from common.constants import filter_words
from django.core.management.base import BaseCommand
from wordcloud import WordCloud

from jobsearch_project.settings import BASE_DIR


class Command(BaseCommand):
    help = '채용공고에서 title을 기반으로 워드클라우드를 생성합니다.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            help='워드클라우드에 활용될 채용공고 수를 지정합니다. (기본값 500)',
            default=500
        )

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        nouns = []
        job_posts = pd.read_csv("jobs_postings.csv")[1:count]
        for idx, post in job_posts.iterrows():
            try:
                current = extract_korean_nouns(post["title"]) + extract_english_nouns(post["title"])
                nouns += current
            except Exception:
                print(post["title"])
                continue

        self.stdout.write(f'처리할 공고 수: {len(job_posts)}건')
        self.stdout.write('텍스트 처리 중... (영어/한국어 명사 추출)')

        self.stdout.write('명사 정규화 처리 중...')
        year_normalized = format_years(nouns)
        normalized = [normalize_phrase2(p) for p in year_normalized]
        counter = Counter(normalized)
        counter = Counter(
            {
                k: v for k, v in counter.items()
                if v >= 5 and k not in filter_words
            }
        )

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
        output_path = f'{dir_path}/wordcloud_title.png'
        wordcloud.to_file(output_path)
        self.stdout.write(self.style.SUCCESS(f'워드클라우드 저장 완료: {output_path}'))
        self.stdout.write(self.style.SUCCESS("작업이 성공적으로 완료되었습니다."))
