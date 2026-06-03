FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PORT=8501

WORKDIR /app

# system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential git ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# install poetry and project deps from pyproject.toml
RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-interaction --no-ansi --no-dev || true

# app
COPY . /app

EXPOSE ${PORT}

# Streamlit entry (use app.py under package)
CMD ["streamlit", "run", "ai_media_generator/app.py", "--server.port", "${PORT}", "--server.address", "0.0.0.0"]
