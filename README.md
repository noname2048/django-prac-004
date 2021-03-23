# Django Portfolio

[![django-prac-004](https://circleci.com/gh/noname2048/django-prac-004.svg?style=shield)](https://circleci.com/gh/noname2048/django-prac-004)
[![codecov](https://codecov.io/gh/noname2048/django-prac-004/branch/main/graph/badge.svg?token=S44312H93C)](https://codecov.io/gh/noname2048/django-prac-004)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Django 연습 레포 입니다.

## 1 서버개요

다이어그램

### 1.1 메인 기술 스택

* `Django: 3.1.5`
* `postgresSQL: 12.5`
* `circleci: 2.1`
* `codecov: py-v2.1.11`
* `docker v20.10.6` `docker-compose v1.25.5` `compose file format 3.8`
* `poetry 1.1.5`

### 1.2 구현된 기능

#### 1.2.1 서버 내부관련 기능

* 로그인
* 비밀번호 찾기 (구현중)

#### 1.2.2 서버 외부관련 기능

* circleci + python manage.py test
* postgres (aws rdb)
* media file (aws s3, file field) `django-storages` `boto3`
* test coverage `codecov`
* aws application load balance `aws alb`
* client - (ssl) - alb - (http) - nginx - (socket) - gunicorn - (wsgi) - django
* postcss를 이용한 tailwind 도입

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
* 프론트 + vercel
* 문자 인증
* google 혹은 github 로그인
* github혹은 discus 덧글 지원기능
* google analytics
* EKS
* subdomain
* open graph
  
## 2 테스트용 서버 실행

테스트 서버 다이어 그램

### 2.1 테스트 환경

* 레포 루트에서 `docker-compose up` 을 이용하여 테스트
* 장고 환경(컨테이너)은 `Docerfile.django.dev` 이용하여 직접 빌드
* 로컬에 postgresql 을 5431:5432 로 띄워 테스트
* redis-server 6378:6379 로 테스트
* static과 media 파일은 S3 이용

### 2.2 테스트 환경변수

docker-compose.yml 에서 장고 컨테이너 up 시에 레포루트의 .env 를 참조함 (클론시 생성필요)

장고 기본 \
`DEBUG_DJANGO_SECRECT_KEY`

도커 관련 \
`DEBUG_POSTGRES_DB_HOST` `DEBUG_POSTGRES_DB_USER` `DEBUG_POSTGRES_DB_PORT` `DEBUG_POSTGRES_DB_PASSWORD`

ASW IAM 관련 \
`DEBUG_S3_AWS_ACCESS_KEY_ID` `DEBUG_S3_AWS_SECRET_ACCESS_KEY` `DEBUG_S3_AWS_STORAGE_BUCKET_NAME`

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

배포 다이어그램

### 4.1 배포과정

1. git push
2. circleci build
3. circleci -> aws s3 (code)
   
### 4.2 배포용 환경변수

현재는 ec2에 직접 scp로 .env 파일 전달하여 systemd service 파일에 EnvironmentFile 로 전달

* PRODUCT_DJANGO_SECRECT_KEY
* PRODUCT_DJANGO_ALLOWED_HOSTS
* PRODUCT_POSTGRES_DB_HOST
* PRODUCT_POSTGRES_DB_USER
* PRODUCT_POSTGRES_DB_PORT
* PRODUCT_POSTGRES_DB_PASSWORD
* PRODUCT_DJANGO_SUPERUSER_NAME
* PRODUCT_DJANGO_SUPERUSER_EMAIL
* PRODUCT_DJANGO_SUPERUSER_PASSWORD

### 4.3 nginx 관련



### 4.4 gunicorn 관련



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
