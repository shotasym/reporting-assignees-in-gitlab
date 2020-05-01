DOCKER_COMPOSE_PATH := ./docker-compose.yml

.PHONY: build
build:
	docker-compose -f ${DOCKER_COMPOSE_PATH} build

.PHONY: up
up:
	docker-compose -f ${DOCKER_COMPOSE_PATH} up

.PHONY: down
down:
	docker-compose -f ${DOCKER_COMPOSE_PATH} down
