FROM python:3.13-slim

RUN mkdir /runtime
COPY requirements.txt /runtime

RUN pip install -r /runtime/requirements.txt

COPY main.py /runtime

WORKDIR /runtime

CMD hypercorn main:app --reload -b 0.0.0.0
