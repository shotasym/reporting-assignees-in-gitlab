FROM python:3.7.4-slim-stretch

COPY Pipfile Pipfile.lock /
COPY reporting_assignees_in_gitlab.py /

RUN pip install -U pip pipenv \
    && pipenv install --system

ENTRYPOINT ["python", "/reporting_assignees_in_gitlab.py"]
