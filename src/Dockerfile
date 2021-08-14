FROM python:3.8-slim-buster

RUN mkdir -p /src/

COPY Pipfile* /src/
# RUN cd /src/ && \
#     pip install pipenv && \
#     # pipenv install --system --deploy --ignore-pipfile

COPY . /src/
WORKDIR /src/

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

CMD ["gunicorn", "-w", "3", "--bind", ":8000", "config.wsgi:application"]
