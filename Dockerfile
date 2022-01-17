FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /slack
COPY requirements.txt /slack/requirements.txt
RUN python -m pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /slack/requirements.txt

COPY src /slack/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload","--log-level debug", "--port", "3000"]
