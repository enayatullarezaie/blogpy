FROM python:3.11
LABEL MAINTAINER="enayatulla rezaie"

RUN mkdir /drf
WORKDIR /drf
COPY . /drf

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
EXPOSE 8000

ADD ./requirements/requirements.txt /drf
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /drf/requirements/requirements.txt
RUN python app/manage.py collectstatic --no-input



CMD [ "gunicorn", "--chdir", "app", "--bind", ":8000", "app.config.wsgi:application" ]


