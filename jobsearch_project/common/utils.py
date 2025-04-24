import re
import platform
from typing import Dict, List, Optional

import nltk
from konlpy.tag import Hannanum
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from common.constants import position_map

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
    return position_map.get(phrase, None)


def normalize_phrase2(phrase: str) -> str:
    """
    위의 표준화 함수와 같은 기능을 하나,
    해당하는 단어가 dict내에 없을 경우 오리지널 문자열을 내려주는 함수
    """
    phrase = phrase.lower()
    return position_map.get(phrase, phrase)


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


def format_years(strings: List[str]) -> List[str]:
    """
    요구 경력의 경우 숫자만 리턴되는 경우가 잦아
    이미 명사 분류가 끝난 리스트를 받아
    10이하의 int형에 한해서 '{int}년이상'의 형태로 만들어주는 함수
    """
    result = []
    for s in strings:
        match = re.search(r'(\d+)', s)
        if match:
            num = int(match.group(1))
            if num > 0 and num <= 10:
                result.append(f'{num}년이상')
            else:
                result.append(s)
        else:
            result.append(s)
    return result
