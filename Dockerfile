FROM python:3.12-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# copy the application into the container
COPY . /app

# install the application dependencies
WORKDIR /app
RUN uv sync --frozen --no-cache

# run the app
CMD ["uv", "run", "/app/main.py"]
