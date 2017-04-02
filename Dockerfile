FROM python:3.5

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:5000 pylint_server:create_app\(\)