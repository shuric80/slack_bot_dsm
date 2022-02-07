FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

#RUN addgroup --system slack_user && \
#    adduser --system --group slack_user
#USER slack_user

WORKDIR /slack
COPY . /slack

RUN python -m pip install --upgrade pip && pip install --no-cache-dir --no-deps -r /slack/requirements.txt

CMD ["uvicorn", "src.main:api", "--host", "0.0.0.0", "--reload", "--port", "3000"]
