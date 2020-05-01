import slackweb
import requests
import re
import os
from urllib.parse import urlparse
from datetime import datetime, timedelta
from typing import List

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
GITLAB_API_URL = "https://" + os.environ.get("GITLAB_DOMAIN") + "/api/v4"
GITLAB_ASSIGNEE_ID = os.environ.get("GITLAB_ASSIGNEE_ID")
GITLAB_PRIVATE_TOKEN = os.environ.get("GITLAB_PRIVATE_TOKEN")

slack = slackweb.Slack(url=SLACK_WEBHOOK_URL)


def push_slack_message(messages: List[str]):
    slack.notify(text="\n".join(messages))


def get_gitlab_contents(url: str):
    results = []

    def _set_contents(url: str):
        res = requests.get(url, headers={"Private-Token": GITLAB_PRIVATE_TOKEN})
        if res.status_code != 200:
            raise Exception("status_code is %d" % res.status_code)

        data = res.json()
        if type(data) is list:
            results.extend(data)
        elif type(data) is dict:
            results.append(data)

        link = re.search(r'<(?P<next>.*)>; rel="next"', res.headers.get("link"))
        if link and link.group("next"):
            _set_contents(link["next"])

    _set_contents(url)
    return results


def get_gitlab_issues_opened(assignee_id: int):
    return get_gitlab_contents(
        GITLAB_API_URL + f"/issues?scope=all&assignee_id={assignee_id}&state=opened"
    )


def get_gitlab_mr_opened(assignee_id: int):
    return get_gitlab_contents(
        GITLAB_API_URL
        + f"/merge_requests?scope=all&assignee_id={assignee_id}&state=opened"
    )


def jst_strftime(utc_t: datetime) -> str:
    return (utc_t + timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")


GITLAB_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def create_slack_messages() -> List[str]:
    messages = []
    messages.append("ReportDate: %s" % datetime.now().date())
    messages.append("\n")

    messages.append("================ Issues ================")
    for issue in get_gitlab_issues_opened(GITLAB_ASSIGNEE_ID):
        messages.append("title: %s" % issue["title"])
        messages.append(
            "created_at: %s"
            % jst_strftime(
                datetime.strptime(issue["created_at"], GITLAB_DATETIME_FORMAT)
            )
        )
        messages.append("due_date: %s" % issue["due_date"])
        messages.append("labels: %s" % issue["labels"])
        messages.append("web_url: %s" % issue["web_url"])
        messages.append("\n")

    messages.append("================ MR ================")
    for issue in get_gitlab_mr_opened(GITLAB_ASSIGNEE_ID):
        messages.append("title: %s" % issue.get("title"))
        messages.append(
            "created_at: %s"
            % jst_strftime(
                datetime.strptime(issue["created_at"], GITLAB_DATETIME_FORMAT)
            )
        )
        messages.append("labels: %s" % issue["labels"])
        messages.append("web_url: %s" % issue["web_url"])
        messages.append("\n")

    return messages


push_slack_message(create_slack_messages())
