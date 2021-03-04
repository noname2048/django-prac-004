# django-prac-004:dev
[![django-prac-004](https://circleci.com/gh/noname2048/django-prac-004.svg?style=svg)](https://circleci.com/gh/noname2048/django-prac-004.svg?style=svg)

벡엔드의 여러가지를 연습하고자 만든 저장소 입니다.

## 1 서버개요
### 1.1 구현된 기능
* circleci + python manage.py test (메인 화면 테스트)
* default DB: AWS RDS (postgres)
* FileField: AWS S3 (django-storages, boto3)

### 1.2 구현할 기능
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
* codecov 이용해보기

### 1.3 서버구조
-> (http) nginx (socket) gunicorn (wsgi) django \
(rdbms) postgresql \
(nosql: cache) redis \
(nosql: persistance) mongodb
## 2 서버실행
### 2.1 환경변수와 키값
secret 대신 env 파일 이용
루트 폴더 아래에 해당 파일과 키들 필요
```
# django-prac-004/.secrets.json
{
    "DJANGO_SECRET_KEY": ""
    "ALLOWED_HOSTS": [
        ""
    ]
}
```
### 2.2 도커 컴포즈 파일로 실행
--build 옵션: 이미지 빌드과정을 터미널에서 보여줌
```bash
docker-compose up --build
```
## 3 VCS 관리
### 3.1 commit message abbreviation
* \+ 추가 add
* \- 제거 remove
* \* 수정 update
* \~ 이동 moved

### 3.2 formatters
* python: black
* html: prettier


## 4. tips
### 4.1 환경변수 관련
dotenv 사용
#### 환경변수가 없을때
os.environ["key"] | "KeyError"
os.environ.get("key") | "None"
os.getenv("key") | ""
os.getenv("key", "default_value") | "default_value"
