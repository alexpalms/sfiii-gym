FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

RUN uv venv
RUN uv pip install -e . --group dev

CMD ["/bin/bash", "docker/entrypoint.sh"]
