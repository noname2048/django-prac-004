# Django Portfolio

[![django-prac-004](https://circleci.com/gh/noname2048/django-prac-004.svg?style=shield)](https://circleci.com/gh/noname2048/django-prac-004?branch=main)
[![codecov](https://codecov.io/gh/noname2048/django-prac-004/branch/main/graph/badge.svg?token=S44312H93C)](https://codecov.io/gh/noname2048/django-prac-004)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Django 연습 레포 입니다. 21.03.04 ~ 21.04.15 까지 서비스 하였습니다. \
비용문제로 더 좋은 서비스로 돌아오겠습니다. \
[https://www.noname2048.dev](https://www.noname2048.dev)

## 1. 서버개요
![](/presentation/스크린샷,%202021-04-15%2018-50-13.png)

![](/presentation/스크린샷,%202021-04-15%2018-50-50.png)

![](presentation/스크린샷,%202021-04-15%2022-50-36.png)

![](presentation/스크린샷,%202021-04-15%2018-24-51.png)

![](presentation/스크린샷,%202021-04-15%2018-26-03.png)

![](presentation/스크린샷,%202021-04-15%2018-33-17.png)

다이어그램

### 1.1 메인 기술 스택

* `Python 3.8.8` `Poetry 1.1.5`
* `docker v20.10.5` `docker-compose v1.28.5` `Compose file 3.8`
* `django: 3.1.7`
* `postgresSQL: 12.5`
* `circleci: 2.1`
* `codecov: py-v2.1.11`
* `awscli/2.1.31 Python/3.8.8`

### 1.2 기능구현 (service feature)

#### 1.2.1 서버 내부관련 기능

* 로그인 여러번 시도 해도 성공하면 redirect back 을 이용한 정상 복귀
* tailwind css 로 스타일링 하기
* 자동 태그 처리
* 조회수 기능 (해당 IP가 6시간 내에 보았거나 / 해당 USER가 6시간내에 봤으면 무효) 
* 페이지네이션 커스텀
* open graph (글마다로 고칠 것) 

#### 1.2.2 서버 외부관련 기능

* CI, circleci + codecov
* CD, circleci + aws codedeploy (ec2 nginx blue-green, not gracefull)
* RDBS postgres (aws rdb, 한달에 3만원)
* AWS S3 (static files + media file) `django-storages`
* SSL (namecheap positive SSL)
* Load Balance (aws alb, nginx)

### 1.3 구현할 기능
* 글과 덧글을 수정하고 생성할 때 IP history 추가하기.
* 비밀번호 찾기
* key-value memory cache: redis (aws elasticache, cost...?)
* document type nosql: mongodb
* static files: aws cloudfront
* test 경험: (unittest), pytest
* JWT 토큰 - 프론트 지원
* restframework - 우리집 책장 API
* 비동기 태스크 큐: celery - sendgrid(mail)
* 특정 app별로 media file 분리된 버킷에 업로드(돈이 없다 - 나중에)
* SEO (search engine optimization: root.txt 외 기타)
* 프론트 + vercel
* google 혹은 github 로그인
* github혹은 discus 덧글 지원기능
* google analytics
* reStructedText 로 문서 작성 (rst 지원 앱들이 별로 없다 - 보류)
* cookie를 이용한 ..?
* grapql relay
* post model 내부에 카테고리 이름과 작성자 이름 반정규화 하기

### 1.4 돈벌면 구현할 기능

* RDB failover
* twilio 문자인증
* EKS autoscale
* subdomain
* multi-DB

## 2. 개발환경

docker-compose를 통한 환경 통합관리

![](presentation/스크린샷,%202021-04-17%2001-10-30.png)

### 2.1 개발용 서비스 띄우기

* 폴더 루트에서 `docker-compose up` 을 이용하여 개발 서버 작동
* 장고 환경(컨테이너)은 `Docerfile.django.dev` 이용하여 직접 빌드
* 로컬에 postgresql 을 5431:5432 로 띄워 테스트
* redis-server 6378:6379 로 테스트
* static과 media 파일은 S3 이용

#### 2.1.1 개발용 서비스 상세개요

* docker 3개, 각 django, postgresql, redis
* django는 dockerfiles/Dockerfile.django.dev 로 빌드, 나머지는 이미지 이용
* 혹시 모르니 postgresql, redis는 host post를 -1 하여 우회
* S3, static files는 배포환경과 공유
* 
### 2.1.2 개발용 서비스에 필요한 환경 변수

* docker-compose.yml 에서 장고 컨테이너 up 시에 레포루트의 .env 를 참조함 (클론시 생성필요)
* .gitignore 되어 있으므로 직접 repo root 폴더 안에 .env 만들어야함
* KeyError raise 시 아래 환경 참고

Django \
`DEBUG_DJANGO_SECRECT_KEY`

DB 관련 \
`DEBUG_POSTGRES_DB_HOST` `DEBUG_POSTGRES_DB_USER` `DEBUG_POSTGRES_DB_PORT` `DEBUG_POSTGRES_DB_PASSWORD`

(차후 개발 환경에서는 static files를 업로드 하지 않은 상태에서 사용할 수 있도록 변경)
ASW IAM 관련 \
`DEBUG_S3_AWS_ACCESS_KEY_ID` `DEBUG_S3_AWS_SECRET_ACCESS_KEY` `DEBUG_S3_AWS_STORAGE_BUCKET_NAME`

## 3. 테스트 환경 (CI)

### 3.1 테스트 환경 띄우기

* main PR을 받을때만 해당 테스트 진행
* .circleci/config.yml 을 이용하여 circleci 에서 작동
* jobs는 한개로 이루어져 있으며, 총 3개의 docker를 사용 (django, db1, cache1)
* 서버가 띄워지면 python manage.py test 호출
* test를 coverage 파악후 codecov로 제출
* 이후 aws codedeploy 에 deploy cli 호출

### 3.2 테스트 환경변수

select * from 개발환경변수 \
union \
`CODECOV_TOKEN` `CIRCLECI_DJANGO_ACESS_ID` `CIRCLECI_DJANGO_ACESS_KEY` 

codecov 전송용 토큰 및 circleci 에서 ec2 및 codedeploy 관련 role 이 설정된 user

## 4. 배포환경 (CD)

* EC2 free tier 이용 (12개월 초과함, 다시 아이디 새로파기)
* EC2 에 nginx를 설치하고, gunicorn이 탑재된 docker 준비
* codedeploy를 통해 deploy.sh 실행
* blue가 실행중이였으면 green을 실행한뒤, blue를 종료
* nginx는 blue와 green에 대해 모두 listening

### 4.1 배포환경변수

EC2에서 .env 파일을 env_file로 넘겨줌

* `PRODUCT_DJANGO_SECRECT_KEY` `PRODUCT_DJANGO_ALLOWED_HOSTS`
* `PRODUCT_POSTGRES_DB_HOST` `PRODUCT_POSTGRES_DB_USER` `PRODUCT_POSTGRES_DB_PORT` `PRODUCT_POSTGRES_DB_PASSWORD`
* `PRODUCT_DJANGO_SUPERUSER_NAME` `PRODUCT_DJANGO_SUPERUSER_EMAIL` `PRODUCT_DJANGO_SUPERUSER_PASSWORD`
* `PRODUCT_S3_AWS_ACCESS_KEY_ID` `PRODUCT_S3_AWS_SECRET_ACCESS_KEY` `PRODUCT_S3_AWS_STORAGE_BUCKET_NAME`

### 4.2 nginx, gunicorn 설정

* django-prac-004/nginx 참조
* 기본 설치된 nginx에 proxy_pass 로 gunicorn 도커로 호스팅
* 호스팅 과정에서 Http Header 관련 설정
* gunicorn은 upstream으로 blue(-p 8001), green(-p 8002) 감시
* gunicorn 설정은 docker-compose.blue.yml 에 명시 (--workers=2)

## 5 Version Control System 관련사항

### 5.1 formatter 를 이용한 정리

코드를 깨끗이 관리하기 위해 코드 save 시에 formatter 호출

대상 | formatter
--- | ---
`python` | `black`

### 5.2 커밋 메세지 관련 (권장)

commit message abbreviation
`20.03.15: v4`
prefix | 기호 | feature | 기호 | postfix
--- | --- | --- | --- | ---
newfile | `+` | readme | `+` | feature added
file removed | `-` | readme | `-` | feature removed
&nbsp; | &nbsp; | readme | `#` | feature updated 
file moved | `~` | readme | &nbsp; | &nbsp;

## 6 오류처리

### 6.1 환경변수관련

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
