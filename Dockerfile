FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
WORKDIR /slack
COPY . /slack

RUN python -m pip install --upgrade pip && pip install --no-cache-dir --upgrade -r /slack/requirements.txt

CMD ["uvicorn", "src.main:api", "--host", "0.0.0.0", "--reload", "--port", "3000"]
