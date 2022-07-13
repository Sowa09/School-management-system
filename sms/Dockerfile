FROM python:3.8

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY . /opt/app

RUN pip install gunicorn

CMD gunicorn --bind=0.0.0.0:8080 sms.wsgi


