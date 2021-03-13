# Django Portfolio

[![django-prac-004](https://circleci.com/gh/noname2048/django-prac-004.svg?style=shield)](https://circleci.com/gh/noname2048/django-prac-004)
[![codecov](https://codecov.io/gh/noname2048/django-prac-004/branch/main/graph/badge.svg?token=S44312H93C)](https://codecov.io/gh/noname2048/django-prac-004)

Django 연습 레포 입니다.

## 1 서버개요

### 1.1 메인 기술 스택

* `Django: 3.1.5`
* `PostgresSQL: 12.5`
* `CircleCi: 2.1`
* `Codecov: py-v2.1.11`

### 1.2 구현된 기능

* circleci + python manage.py test (메인 화면 테스트)
* default DB: AWS RDS (postgres)
* FileField: AWS S3 (django-storages, boto3)
* Codecov 연동

### 1.3 구현할 기능

* CD(Continuos Delivery) DA(deploy automation?)
* Replica RDB (RDB failover...?)
* memory nosql: redis (aws elasticache)
* disk nosql: mongodb
* static files: aws s3 : cloudfront
* media S3 : aws s3
* test 경험 :unittest, pytest
* JWT 토큰
* 비동기 태스크 큐: celery - sendgrid(mail)
* images와 files 분리된 버킷에 업로드
* multiDB로 여러가지 DB 한꺼번에 써보기
* product 에서 nginx(http), gunicorn(socket), django(wsgi) 쓰기
* redis와 mongodb 연결하기

## 2 테스트용 서버 실행

### 2.1 테스트 환경

* python manage.py runserver 을 이용하여 테스트
* 로컬에 postgresql 을 5431 로 띄워 테스트 (5432는 이미 설치된 postgresql 이 있다고 가정)
* 테스트에서 바로 프로덕션 S3 접속 (나중에 공부해서 분리)
* Redis 준비

### 2.2 테스트 환경변수

local에서는 pypi의 dotenv를 사용하여 프로젝트 폴더의 .env를 읽습니다.
python manage.py runserver 에서 필요한 환경변수는 다음과 같습니다.

키 | 관련 | 비고
---|---|---
DJANGO_SECRET_KEY | 장고 기본
PRODUCT_DB_POSTGRES_HOST | AWS DB
PRODUCT_DB_NAME | AWS DB
PRODUCT_DB_PASSWORD | AWS DB
AWS_ACCESS_KEY_ID | AWS S3
AWS_SECRET_ACCESS_KEY | AWS S3

### 2.3 도커 컴포즈 파일로 실행

dockerfile 내부의 docker-compose.dev.yml 를 프로젝트 파일 아래의 docker-compose.yml 로 변경
이후 up 명령어 실행

```bash
docker-compose up --build .
```

## 3 Version Control System 관련사항

### 3.1 formatter 를 이용한 정리

formatter|대상
---|---
black: python
prettier: html, js

### 3.2 커밋 메세지 관련 (중요하지 않음)

(commit message abbreviation)
`20.03.11: v3`
기호|prefix|postfix
---|---|---
\+|new file|feature added|
\-|file removed|feature removed|
\#||updated
\>|file moved|

## 4. 배포환경

### 4.1 배포과정

1. git push
2. circleci build
3. circleci -> aws s3 (code)
   
### 4.2 배포용 환경변수

#### 4.2.1 circleci

--

#### 4.2.2 aws ec2

--

## 5 오류처리

### 5.1 환경변수

python에서 env를 가져오는 4가지 방법중에, 키가 없으면 오류가 나는 방식을 채택하였습니다. \
KeyError 오류가 난다면 해당 키 항목의 키 체크가 필요합니다.

```python
# <key> <default_value> is abstarcted

# 함수의 원형 os.getenv("<key>", default=None) 
os.getenv("<key>") # IF_NOT: "None"
os.getenv("<key>", "<default_value>") # IF_NOT: "<default_value>"
os.environ["<key>"] # IF_NOT: KeyError raise # This repo choose this method
os.environ.get("key") # IF_NOT: "None"
```
