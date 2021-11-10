all: build down migrate collectstatic up

pull:
	docker-compose pull

push:
	docker-compose push

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	docker-compose run app bash -c '/wait && python manage.py migrate $(if $m, api $m,)'

createsuperuser:
	docker-compose run app bash -c '/wait && python manage.py createsuperuser'

collectstatic:
	docker-compose run app bash -c '/wait && python manage.py collectstatic --no-input'

makemigrations:
	docker-compose run --volume=${PWD}/src:/src app bash -c '/wait && python manage.py makemigrations'
	sudo chown -R ${USER} src/api/migrations/

psql:
	docker exec -it dt-is-backend_db psql -U postgres

celery:
	docker-compose run celery

celerybeat:
	docker-compose run celerybeat

dev:
	docker-compose run --volume=${shell pwd}/src:/src --publish=8000:8000 app bash -c '/wait && python manage.py runserver 0.0.0.0:8000'

dev_plus:
	docker-compose run --volume=${shell pwd}/src:/src --publish=8000:8000 app bash -c '/wait && python manage.py runserver_plus --print-sql 0.0.0.0:8000'

dev_test:
	docker-compose run --volume=${shell pwd}/src:/src app bash -c '/wait && pytest'

swagger_build:
	docker-compose run --volume=${PWD}/swagger:/app/swagger app python /app/swagger/compile.py
	sudo chown -R ${USER} swagger/build/

swagger_dev:
	docker-compose run --volume=${PWD}/swagger/build:/swagger --publish=8080:8080 swagger

update_or_create_user_groups:
	docker-compose run app bash -c '/wait && python manage.py update_or_create_user_groups'

get_incomes_and_expenses_by_company_account:
	docker-compose run app bash -c '/wait && python manage.py get_incomes_and_expenses_by_company_account'

command:
	docker-compose run --volume=${PWD}/src:/src  app python manage.py ${c}

shell:
	docker-compose run app python manage.py shell

vacation:
	docker-compose run app bash -c '/wait && python manage.py vacation'

test:
	docker-compose run app pytest

debug:
	docker-compose run app bash -c '/wait && python manage.py debug'

piplock:
	docker-compose run --rm --no-deps --volume=${PWD}/src:/src --workdir=/src app pipenv install
	sudo chown -R ${USER} src/Pipfile.lock

.PHONY: all build up down migrate makemigrations dev psql celery celerybeat dev_test update_or_create_user_groups vacation test debug swagger_build swagger_dev dotenv
.
.
.
.
.