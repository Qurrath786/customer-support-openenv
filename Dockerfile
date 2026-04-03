FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir openenv-core uvicorn

CMD ["python", "-m", "openenv.server"]