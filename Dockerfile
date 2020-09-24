FROM python:3.7-alpine

WORKDIR /app

COPY ./app/requirements.txt  /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./app /app

EXPOSE 80
EXPOSE 443

CMD ["python", "/app/main.py"]