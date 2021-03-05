FROM python:3.9.2
LABEL version="1.0" \
    description="simple django Dockerfile"

COPY ./requirements.txt .
RUN apt-get update && pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

COPY ./django_app /app
COPY ./.secrets.json /
COPY ./entrypoint.sh /
WORKDIR /app

RUN sh ../entrypoint.sh
CMD ["python", "manage.py", "runserver", "0:8000"]
