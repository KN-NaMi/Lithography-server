FROM nvcr.io/nvidia/l4t-base:r36.2.0

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv curl git build-essential \
    python3-pygame \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip \
    && pip3 install uv

WORKDIR /app

COPY pyproject.toml uv.lock* ./
COPY . .

RUN uv sync --no-dev --frozen

CMD ["uv", "run", "python", "main.py"]