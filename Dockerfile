FROM python:latest
MAINTAINER windfarer <windfarer@gmail.com>

RUN mkdir /counter
COPY . /counter
WORKDIR /counter

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 80
ENTRYPOINT ["gunicorn","-w 4", "-b 0.0.0.0:80", "counter:app"]
