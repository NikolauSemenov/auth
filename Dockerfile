FROM python:3.13-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

ARG POETRY_VERSION=2.2.1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==${POETRY_VERSION}"
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY src /app/src/
COPY alembic.ini /app/
COPY migrations /app/migrations

CMD ["python", "src/run.py"]
