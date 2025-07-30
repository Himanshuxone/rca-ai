# ---------- Stage 1: Builder ----------
FROM python:3.11-alpine as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies
RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    python3-dev \
    build-base

# Copy requirements and install
COPY requirements.txt .
RUN pip install --prefix=/usr/local -r requirements.txt

# Copy app code
COPY . .

# ---------- Stage 2: Runtime ----------
FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache libpq

# Copy everything
COPY --from=builder /usr/local /usr/local
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
