FROM python:3.5

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY src /app/src
VOLUME ["/app/src"]

WORKDIR /app/src
EXPOSE 5000
CMD gunicorn -b 0.0.0.0:5000 pylint_server:create_app\(\)