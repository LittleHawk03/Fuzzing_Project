FROM ubuntu:latest

RUN apt-get update\
    && apt-get install python3 -y\
    && apt-get install python-is-python3 -y\
    && apt-get install python3-pip -y\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/root/fuzzing

ADD ./ /home/root/fuzzing

RUN pip install -r requirements.txt
