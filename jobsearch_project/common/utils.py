import platform
from typing import Dict, List, Optional

import nltk
from konlpy.tag import Hannanum
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def normalize_phrase(phrase: str) -> Optional[str]:
    """
    주어진 직무 관련 키워드를 표준화된 형태로 변환
    
    Args:
        phrase (str): 입력 키워드 문자열
        
    Returns:
        Optional[str]: 표준화된 키워드 또는 None (매칭되지 않을 경우)
    """
    position_map = {
        '백': 'backend',
        '백엔드': 'backend',
        '백엔드개발자': 'backend',
        'backend': 'backend',
        'back': 'backend',
        'back-end': 'backend',
        'node': 'backend',
        'nodejs': 'backend',
        'django': 'backend',
        'flask': 'backend',
        'fastapi': 'backend',
        'nest': 'backend',
        'nestjs': 'backend',
        'spring': 'backend',
        'java': 'backend',
        'golang': 'backend',
        'go': 'backend',
        'kotlin': 'backend',
        'php': 'backend',
        '.net': 'backend',
        'ruby': 'backend',
        'ruby on rails': 'backend',
        '프론트': 'frontend',
        '프론트개발자': 'frontend',
        '프론트엔드': 'frontend',
        'front': 'frontend',
        '프론트엔지니어': 'frontend',
        '프런트엔드': 'frontend',
        'front-end': 'frontend',
        'frontend': 'frontend',
        'react': 'frontend',
        'react.js': 'frontend',
        'vue': 'frontend',
        'vue.js': 'frontend',
        'angular': 'frontend',
        'typescript': 'frontend',
        'html': 'frontend',
        'css': 'frontend',
        'javascript': 'frontend',
        'js': 'frontend',
        'nextjs': 'frontend',
        'next': 'frontend',
        '유니티': 'unity',
        'unity': 'unity',
        '유니티개발자': 'unity',
        '운영': '운영',
        '매니저': '운영',
        '데이터': 'Data',
        'data': 'Data',
        '빅데이터': 'Data',
        '관리': '관리',
        '웹개발자': 'web',
        '웹개발': 'web',
        '웹': 'web',
        'web': 'web',
        'ai': 'AI',
        '인공지능': 'AI',
        '인공': 'AI',
        '블록체인': 'Blockchain',
        '블록': 'Blockchain',
        'blockchain': 'Blockchain',
        '하드웨어': 'hardware',
        'hardware': 'hardware',
        '데브옵스': 'Devops',
        '브옵스': 'Devops',
        'devops': 'Devops',
        'ios': 'App',
        'android': 'App',
        '앱개발': 'App',
        '앱': 'App',
        '안드로이드': 'App',
        'flutter': 'App',
        'reactnative': 'App',
        'react native': 'App',
        '스위프트': 'App',
        'swift': 'App',
        'kotlin': 'App',
        'java(android)': 'App',
        'sre': 'SRE',
        '컨설턴트': '컨설턴트',
        '서버개발자': 'Server',
        '서버개발': 'Server',
        '서버': 'Server',
        'server': 'Server',
        '풀스택': 'fullstack',
        '풀스택개발자': 'fullstack',
        '풀스택엔지니어': 'fullstack',
        'fullstack': 'fullstack',
        'full-stack': 'fullstack',
        'pytorch': 'AI',
        'tensorflow': 'AI',
        '머신러닝': 'AI',
        '딥러닝': 'AI',
        'machine learning': 'AI',
        'deep learning': 'AI',
        '데이터사이언티스트': 'Data',
        '데이터사이언스': 'Data',
        'data scientist': 'Data',
        '데이터분석': 'Data',
        '데이터엔지니어': 'Data',
        '데이터분석가': 'Data',
        'ci': 'Devops',
        'cd': 'Devops',
        'jenkins': 'Devops',
        'kubernetes': 'Devops',
        'docker': 'Devops',
        '인프라': 'Devops',
        'monitoring': 'Devops',
        'full': 'fullstack',
        'cloud':'cloud',
        '클라우드':'cloud',
        'aws':'cloud',
        'gcp':'cloud',
        'azure':'cloud',
        '아마존': 'cloud',
        '애저': 'cloud',
        '신입': '주니어',
        '주니어': '주니어',
        'junior': '주니어',
        '경력': '시니어',
        '시니어': '시니어',
        'Senior': '시니어',
        '팀장': '시니어'
    }
    return position_map.get(phrase, None)

def extract_korean_nouns(text: str) -> List[str]:
    """
    한글 텍스트에서 명사 추출
    
    Args:
        text (str): 분석할 한글 텍스트
        
    Returns:
        List[str]: 추출된 명사 리스트
    """
    hannanum = Hannanum()
    return hannanum.nouns(text)

def extract_english_nouns(text: str) -> List[str]:
    """
    영어 텍스트에서 명사 추출
    
    Args:
        text (str): 분석할 영어 텍스트
        
    Returns:
        List[str]: 추출된 영어 명사 리스트 (소문자로 통일)
    """
    tokens: List[str] = word_tokenize(text)
    tagged: List[tuple] = pos_tag(tokens)
    return [word.lower() for word, tag in tagged if tag.startswith('NN')]

def get_system_font_path() -> Optional[str]:
    """
    운영체제별 기본 한글 폰트 경로 반환
    
    Returns:
        Optional[str]: 폰트 파일 경로 또는 None (탐색 실패 시)
    """
    system: str = platform.system()
    if system == 'Windows':
        return 'C:/Windows/Fonts/malgun.ttf'
    elif system == 'Darwin':  # macOS
        return '/System/Library/Fonts/AppleGothic.ttf'
    return None