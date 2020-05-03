# reporting-assignees-in-gitlab
reporting assignees in gitlab to slack.

## Usage
```bash
# export env
$ export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxxxxx
$ export GITLAB_DOMAIN=gitlab.ssl.xxxxxx.jp
$ export GITLAB_ASSIGNEE_ID=xx
$ export GITLAB_PRIVATE_TOKEN=xxxx

# build docker image.
$ make build

# run script
$ make run
```
