
FROM python:3.8.8
LABEL description="for EC2 Deploy Django-apps"

RUN apt-get update && apt-get install -y vim wget

COPY ./requirements.txt .
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

CMD ["/bin/bash"]
