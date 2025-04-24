import re

# 하나의 긴 description을 모집분야, 주요업무 등의 카테고리로 나눠서 구조화하는 함수
# 링크드인, 잡코리아만 해당

def format_description_naturally(desc: str) -> str:
    if not desc:
        return ""

    # 한글 바로 뒤에 [ 가 오면 줄바꿈
    desc = re.sub(r'(?<=[가-힣])\[', r'\n[', desc)
    
    # 순수 키워드 정의
    section_keywords = [
        '담당업무 및 자격요건', '지원자격 및 우대사항', '포지션 및 자격요건', '필요기술 및 지원자격',
        '경력 증빙 서류 필수','자격요건 및 우대사항', '기술등급', '주요업무', '담당 업무', '공통 사항',
        '모집분야 및 자격요건', '모집부문 및 자격요건', '지원자격요건', 'Experiences', 'Skill/ Knowledge',
        '주요 업무', '담당업무', '지원자격', '자격요건', '직무소개', '수행업무', '필수조건',
        '우대조건', '우대사항', '기술 스택', '모집부문', '조건', '제출서류', '기술스킬',
        '근무장소', '고용형태', '기타 안내사항', '근무조건', '근무기간', '인원'
    ]
    
    # 한글 뒤 하이픈 → 줄바꿈
    desc = re.sub(r'(?<=[가-힣])-\s*', r'\n- ', desc)
    
    # (3), (12)처럼 괄호 안 숫자 하나일 경우 → 줄바꿈
    desc = re.sub(r'(?<!\n)(\(\d{1,2}\))', r'\n\1', desc)

    # 숫자. 형식 항목 번호 앞에 줄바꿈 (예: 1. ~)
    desc = re.sub(r'(?<!\n)(?<!\d)(\d{1,2}\.)\s*', r'\n\1 ', desc)
    
    # 느낌표 뒤 공백 → 줄바꿈
    desc = re.sub(r'!(\s+)', '!\n', desc)

    # [섹션명] 형태는 줄바꿈만 추가
    for kw in section_keywords:
        desc = re.sub(rf'\[\s*{kw}\s*\]', f'\n\n[{kw}]\n', desc)

    # 순수 키워드는 [키워드]로 감싸기
    for kw in section_keywords:
        desc = re.sub(rf'(?<!\[)({kw})(\s*[-:]?)(?!\])', r'\n\n[\1]\n', desc)
        
    # 마침표 뒤 줄바꿈
    desc = re.sub(r'(?<!\d)\.(?!\))(?=[^a-zA-Z0-9\s])', '.\n', desc)
    
    # 하이픈 + 공백 + [섹션명] → 붙이기
    desc = re.sub(r'-\s+\[', r'- [', desc)

    # 불릿 기호 정리
    desc = re.sub(r'\s*[•●・·–ㆍ]\s*', r'\n- ', desc)

    # 연속 줄바꿈 정리
    desc = re.sub(r'\n{3,}', '\n\n', desc)

    return desc.strip()
