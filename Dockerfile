FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir openenv-core uv

CMD python inference.py && tail -f /dev/null