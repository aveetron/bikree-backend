FROM python:3.9-alpine
RUN mkdir app
RUN cd app
WORKDIR app

COPY . .
RUN pip install -r requirements.txt

