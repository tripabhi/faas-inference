# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /bert-inference

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ src/

COPY app.py app.py


COPY download_models.py download_models.py
RUN chmod +x download_models.py
RUN ./download_models.py


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]