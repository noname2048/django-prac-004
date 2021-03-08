# DJANGO POD
# 공개이미지로 올릴 예정
#
# []: 선택, (): 생략
# [01 BUILD]: 기본적인 파일들만 넣어서 docker를 생성합니다. pip 설치 진행
# (02 MIGRATE): 테스트는 circleci에서, 배포시에는 docker-compose 로 진행
# (03 SERVERRUN): circleci 와 compose 진행

FROM python:3.9.2
LABEL version="1.0" \
    description="simple django Dockerfile"

ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt .
RUN apt-get update && pip install -r requirements.txt

COPY ./django_project ./askbanana/django_project
WORKDIR /askbanana/django_project

CMD ["/bin/bash"]
