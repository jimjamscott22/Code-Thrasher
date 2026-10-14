FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    bubblewrap \
    rustc \
    nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -r -M -s /usr/sbin/nologin codethrasher-sandbox

COPY pyproject.toml ./
COPY app ./app
RUN pip install --no-cache-dir uv && uv pip install --system .

COPY . .

ENV SANDBOX_RUSTC_PATH=/usr/bin/rustc

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
