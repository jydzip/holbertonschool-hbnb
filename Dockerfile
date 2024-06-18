FROM python:3.9-alpine
WORKDIR /app
COPY . /app
RUN pip install -r /app/requirements.txt
ENV PORT 5000
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
VOLUME /app/data