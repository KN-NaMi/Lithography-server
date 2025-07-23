FROM nvcr.io/nvidia/l4t-base:r36.2.0

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip \
    && pip3 install uv

WORKDIR /app

COPY pyproject.toml uv.lock* ./
COPY . .

RUN uv sync --no-dev --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
