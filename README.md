# django-prac-004:dev
[![django-prac-004](https://circleci.com/gh/noname2048/django-prac-004.svg?style=svg)](https://circleci.com/gh/noname2048/django-prac-004.svg?style=svg)

벡엔드의 여러가지를 연습하고자 만든 저장소 입니다.

## 1 서버개요
### 1.1 구현된 개념
* CI; continuous integration; circleci

### 1.2 구현할 개념
* CD? DA(deploy automation?)
* 백업용 RDB
* Redis 캐시서버
* CDN 용 S3 
* media S3
  
### 1.3 서버구조
-> (http) nginx (socket) gunicorn (wsgi) django \
(rdbms) postgresql \
(nosql: cache) redis \
(nosql: persistance) mongodb
## 2 서버실행
### 2.1 환경변수와 키값
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
