FROM python:3.12.7

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt



COPY . /app/
WORKDIR /app