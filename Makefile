app_name = ppt

celery_services = rabbitmq celery
docker_compose := docker compose -f docker-compose.yml

build:
	$(docker_compose) build $(c)

rebuild:
	$(docker_compose) up -d --build --force-recreate $(c)
	docker image prune -f

up:
	$(docker_compose) up -d $(c)

start:
	$(docker_compose) start $(c)

down:
	$(docker_compose) down $(c)

reup:
	$(docker_compose) down $(c)
	$(docker_compose) up -d $(c)

destroy:
	$(docker_compose) down --rmi all -v $(c)

stop:
	$(docker_compose) stop $(c)

restart:
	$(docker_compose) restart $(c)

restart-celery:
	$(docker_compose) restart $(celery_services)

logs:
	$(docker_compose) logs --tail=1000 -f $(c)

app-logs:
	$(docker_compose) logs --tail=1000 -f backend $(c)

celery-logs:
	$(docker_compose) logs --tail=1000 -f celery $(c)

app-bash:
	docker exec -it $(app_name)_backend bash $(c)

db-bash:
	docker exec -it $(app_name)_postgres bash $(c)

createsuperuser:
	docker exec -it $(app_name)_backend python manage.py createsuperuser

collectstatic:
	docker exec -it $(app_name)_backend python manage.py collectstatic -y

migrations:
	docker exec -it $(app_name)_backend python manage.py makemigrations

migrate:
	docker exec -it $(app_name)_backend python manage.py migrate

psql:
	docker exec -it $(app_name)_postgres psql -U postgres

shell:
	docker exec -it $(app_name)_backend python manage.py shell
