# Jobs app management commands

## 워드클라우드 생성 명령 (makewordcloud.py)

* 기능
  * 채용 공고 설명 데이터를 분석하여 워드클라우드 이미지 생성
  * 한글과 영어 명사를 추출하여 빈도수 기반 시각화

* 사용 방법

    ```shell
    python manage.py makewordcloud [options]
    ```

* 옵션
  * --count: 분석할 공고 수 (기본값: 500)

* 예시

    ```bash
    # 기본 옵션으로 실행
    python manage.py makewordcloud

    # 커스텀 옵션으로 실행
    python manage.py makewordcloud --count=200
    ```

* 출력 파일
  * 생성된 이미지: `static/jobs/wordcloud.png.`

* 참고 사항
  1. 한글 처리를 위해 시스템에 한글 폰트가 설치되어 있어야 합니다.
  2. 대량의 데이터를 처리할 경우 시간이 소요될 수 있습니다.


## 채용 경력 비율 분석 명령 (makecareerratio.py)

* 기능
  * 채용 공고에서 '신입'과 '경력' 키워드 빈도 분석
  * 원형 차트(pie chart)로 시각화 결과 저장

* 사용 방법
  
  ```bash
  python manage.py makecareerratio [options]
  ```

* 옵션
  * --count: 분석할 공고 수 (기본값: 500)

* 예시
  
  ```bash
    # 기본 옵션으로 실행
    python manage.py makecareerratio

    # 커스텀 옵션으로 실행
    python manage.py makecareerratio --count=200
    ```

* 출력 파일
  * 생성된 이미지: `static/jobs/career_ratio.png`

* 참고 사항
  1. 한글 처리를 위해 시스템에 한글 폰트가 설치되어 있어야 합니다.
  2. 대량의 데이터를 처리할 경우 시간이 소요될 수 있습니다.
