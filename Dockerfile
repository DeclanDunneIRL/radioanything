FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /

ENV PORT 5000

WORKDIR $APP_HOME

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

# Start the server with gunicorn running main.py
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app