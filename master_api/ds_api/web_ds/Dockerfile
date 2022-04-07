FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /ds
COPY requirements.txt /ds/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /ds/