FROM python:3.13-alpine

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 13856

ENTRYPOINT [ "python", "server.py" ]