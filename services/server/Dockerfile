FROM python:3.11-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv pip install --system

COPY . .

CMD ["uv","run", "main.py"]
