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

## 2 서버실행

### 2.1 환경변수와 키값

local에서는 pypi의 dotenv를 사용하여 프로젝트 폴더의 .env를 읽습니다.
필요한 환경변수는 다음과 같습니다.

키 | 관련 | 비고
---|---|---
DJANGO_SECRET_KEY | 장고 기본
PRODUCT_DB_POSTGRES_HOST | AWS DB
PRODUCT_DB_NAME | AWS DB
PRODUCT_DB_PASSWORD | AWS DB
AWS_ACCESS_KEY_ID | AWS S3
AWS_SECRET_ACCESS_KEY | AWS S3

### 2.2 도커 컴포즈 파일로 실행

local 환경에서는 docker-compose.dev를 이용해 주세요
```bash
docker-compose up --build .
```

* --build: 이미지 빌드과정을 보여줍니다.
* 
## 3 VCS 관리

### 3.1 commit message abbreviation

`20.03.11: v3`
기호|prefix|postfix
---|---|---
\+|new file|feature added|
\-|file removed|feature removed|
\#||updated
\>|file moved|

### 3.2 formatters

* python: black
* html: prettier


## 4. 프로젝트 구동 팁
### 4.1 환경변수 관련

도커를 이용해서 빌드할때 dotenv를 사용하고 있습니다. 필요한 키값은 다음과 같습니다.

### 4.1.1 django-prac-004/.env

| 키 | 관련 | 비고 |
|---|---|---|
| DJANGO_SECRET_KEY | 장고 기본 |
| PRODUCT_DB_POSTGRES_HOST | AWS DB |
| PRODUCT_DB_NAME | AWS DB |
| PRODUCT_DB_PASSWORD | AWS DB |
| AWS_ACCESS_KEY_ID | AWS S3 |
| AWS_SECRET_ACCESS_KEY | AWS S3 |

### 4.1.2 환경변수가 없을때

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
