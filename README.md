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

* circleci + python manage.py test
* postgres (aws rdb)
* media file (aws s3, file field) `django-storages` `boto3`
* code test coverage `codecov`
* aws application load balance `aws alb`
* client - (ssl) - alb - (http) - nginx - (socket) - gunicorn - (wsgi) - django
 
### 1.3 구현할 기능

* CD(Continuos Delivery) DA(deploy automation?)
* Replica RDB (RDB failover...?)
* memory nosql: redis (aws elasticache)
* disk nosql: mongodb
* static files: aws s3 : cloudfront?
* test 경험: (unittest), pytest
* JWT 토큰 - 프론트 지원
* restframework - 우리집 책장 API
* 비동기 태스크 큐: celery - sendgrid(mail)
* 특정 images field 와 file field 를 분리된 버킷에 업로드
* multiDB로 여러가지 DB 한꺼번에 써보기
* redis와 mongodb 연결하기
* autoscale with eks
* SEO (search engine optimization: root.txt 외 기타)
* tailwind 도입
* 프론트 + vercel

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

대상 | formatter
--- | ---
`python` | `black`

### 3.2 커밋 메세지 관련 (중요하지 않음)

#### 3.2.1 commit message abbreviation

`20.03.15: v4`
prefix | 기호 | feature | 기호 | postfix
--- | --- | --- | --- | ---
newfile | `+` | readme | `+` | feature added
file removed | `-` | readme | `-` | feature removed
&nbsp; | &nbsp; | readme | `#` | feature updated 
file moved | `~` | readme | &nbsp; | &nbsp;

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

`<key>` `<default_value>` 는 임의의 str 값이라 가정합니다. \
(ex `"HOST"` `"*"`)

참조방법 | 키가 없을때 | 비고
---|---|---
`os.getenv(<key>)` | None |
`os.getenv(<key>, <default_value>)` | `<default_value>` |
`os.environ[<key>]` | KeyError raised | Choose this method
`os.environ.get(<key>)` | None | 
`os.environ.get(<key>, <default_value>)` | `<default_value>` |
