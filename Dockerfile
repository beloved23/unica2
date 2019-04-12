FROM python:2.7

ENV PYTHONUNBUFFERED 1


WORKDIR .

ADD requirements.txt .

RUN pip install -r requirements.txt