FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /api
WORKDIR /api
COPY requirements.txt /api
RUN pip install -r requirements.txt
COPY . /api
EXPOSE 8000
