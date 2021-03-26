
FROM python:3.8.8
LABEL description="for EC2 Deploy Django-apps"

RUN apt-get update && apt-get install -y vim wget

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py &&\
    python get-poetry.py --yes && \
    rm get-poetry.py
ENV PATH="/root/.poetry/bin:${PATH}"

RUN poetry config virtualenvs.create false

COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry install --no-dev

ENV PYTHONUNBUFFERED 1

CMD ["/bin/bash"]
