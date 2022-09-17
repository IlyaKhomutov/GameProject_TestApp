# syntax=docker/dockerfile:1
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN useradd -ms /bin/bash newuser
USER newuser
WORKDIR /usr/src/test-app

COPY ./requirements.txt /usr/requirements.txt
RUN pip install -r /usr/requirements.txt

COPY . /usr/src/test-app

#EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
