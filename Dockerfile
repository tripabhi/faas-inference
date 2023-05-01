# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /faas-inference

VOLUME /faas-inference/data
ENV DATA_DIR=data

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# RUN mkdir -p models

# CMD [ "python3", "download_models.py" ]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0" ]
