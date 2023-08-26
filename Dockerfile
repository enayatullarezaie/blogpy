FROM python:3.11

RUN apt-get update && \
   apt-get install -y libpq-dev gcc

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
EXPOSE 8000

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/