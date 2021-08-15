FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /src/

RUN apt-get update &&\
    apt-get install -y gdal-bin --no-install-recommends &&\
    rm -rf /var/lib/apt/lists/*

COPY Pipfile* /src/
RUN  cd /src/ &&\
    pip install pipenv &&\
    pipenv lock --keep-outdated --requirements > requirements.txt &&\
    pip install -r /src/requirements.txt

COPY . /src/
WORKDIR /src/

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD ["gunicorn", "-w", "3", "--bind", ":8000", "config.wsgi:application"]
