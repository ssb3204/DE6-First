# Project 1. 채용 정보 분석
## 프로젝트 개요
- 프로그래머스 데이터 엔지니어링 6기 Team 2조 첫번째 프로젝트로, 각종 채용사이트에서 크롤링한 정보를 바탕으로 서울 지역 IT 채용 정보에서 자주 등장하는 키워드를 분석해, 구직자들이 채용 트렌드를 한눈에 알아보기 쉽게 파악할 수 있는 서비스 입니다.

## Installation
- pip 사용 :
```pip install -r requirements```
  - python3.9이상에선 backports.zoneinfo 제외 필요
- poetry 사용
```
poetry add $(cat requirements.txt)
poetry install
```

## 사용 기술 및 라이브러리
  - Python3.x
  - Django Framework
  - SQLite
  - Selenium, beautifulSoup
  - konlpy, nltk
  - pandas, matplotlib


## 프로젝트 역할 분담 및 상세
1. 채용 정보 크롤링
   - 전원 참여 - 사이트별로 분담 
2. 맞춤형 채용 공고 추천(search)
   - 손성배, 양창우 
3. 공고 목록 & 상세 페이지(list)
   - 김현호 
4. 키워드 기반 시각화 - 워드 클라우드 & 차트
   - 정동영, 서미지
