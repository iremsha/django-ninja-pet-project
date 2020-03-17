FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./requirements.txt /tochka/requirements.txt
RUN pip install -r /tochka/requirements.txt

COPY . /tochka/
WORKDIR /tochka/

EXPOSE 8000
