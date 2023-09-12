FROM python:3.11

WORKDIR /app
COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUBUFFERED 1

RUN pip install --upgrade pip && pip install -r requirements/requirements.txt


