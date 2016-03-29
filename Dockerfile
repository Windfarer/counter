FROM python:latest
MAINTAINER windfarer <windfarer@gmail.com>

RUN mkdir /counter
COPY . /counter
WORKDIR /counter

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8000
ENTRYPOINT ["gunicorn","-w 4", "counter:app"]