DOCKER_COMPOSE_PATH := ./docker-compose.yml

.PHONY: build
build:
	docker build -t reporting-assignees-in-gitlab .

.PHONY: run
run:
	docker run --rm \
	--name reporting-assignees-in-gitlab \
	--env SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL} \
	--env GITLAB_DOMAIN=${GITLAB_DOMAIN} \
	--env GITLAB_ASSIGNEE_ID=${GITLAB_ASSIGNEE_ID} \
	--env GITLAB_PRIVATE_TOKEN=${GITLAB_PRIVATE_TOKEN} \
	reporting-assignees-in-gitlab
