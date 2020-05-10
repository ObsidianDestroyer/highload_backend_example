FROM python:3.7-slim

WORKDIR /highload_backend
RUN pip install pipenv==2018.11.26
COPY Pipfile Pipfile.lock ./
RUN pip install pip --upgrade && apt-get update && \
  apt-get install -y --no-install-recommends gcc python-dev && \
  pipenv install --system --deploy && \
  apt-get remove -y gcc python-dev && \
  apt-get autoremove -y

COPY backend backend
COPY backend/app.py .
COPY backend/settings.py .
COPY backend/__init__.py .

EXPOSE 8080
CMD ["uvicorn", "app:app", \
    "--loop", "uvloop", \
    "--host", "0.0.0.0", \
    "--port", "8080", \
    "--log-level", "info", \
    "--limit-max-requests", "55000", \
    "--workers", "3"]
