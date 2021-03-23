# 배포용 ec2에서 작동하는 build
# 프로젝트 홈에서 docker-compose 를 통한 도커 빌드 시행을 가정

FROM python:3.9.2
LABEL description="배포용 장고 도커 파일"

RUN apt-get update && apt-get install -y vim wget

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["/bin/bash"]
