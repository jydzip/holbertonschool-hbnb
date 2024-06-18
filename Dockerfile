FROM python:3.9-alpine
WORKDIR /app

RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
VOLUME /app/data
