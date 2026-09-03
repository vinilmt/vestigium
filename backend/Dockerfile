FROM docker.io/library/python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install uv && uv sync --frozen --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
