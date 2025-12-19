FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app

CMD flask --app "app:create_app" run -h 0.0.0.0 -p $PORT
