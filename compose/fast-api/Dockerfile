FROM python:3.14-slim

WORKDIR /code

COPY pyproject.toml .

RUN pip install --no-cache-dir .

COPY project /code

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
