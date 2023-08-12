FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir pipenv

COPY Pipfile* .

RUN pipenv install --system --deploy

COPY . .

CMD ["python3", "consumer.py"]