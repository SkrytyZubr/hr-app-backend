FROM python:3.12-alpine
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1
RUN apk add --no-cache libpq curl
COPY . /code
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.local/bin/uv pip install --system --no-cache -r pyproject.toml && \
    find /usr/local/lib/python3.12/site-packages/ -name "__pycache__" -type d -exec rm -rf {} + && \
    find /usr/local/lib/python3.12/site-packages/ -name "*.pyc" -delete && \
    rm -rf /root/.local/bin/uv /root/.cache
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]