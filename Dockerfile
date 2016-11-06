##
## Python Dockerfile
##
## Pull base image.
FROM python:2-alpine
MAINTAINER Pete Fincher "pfincher@cisco.com"
EXPOSE 5000

RUN pip install --no-cache-dir setuptools wheel

ADD . /ahod_server1
WORKDIR /ahod_server1
RUN pip install --requirement /ahod_server1/requirements.txt

CMD ["python", "demoapp.py"]

