FROM python:3.11-slim

WORKDIR /workdir

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /workdir/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /workdir/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
