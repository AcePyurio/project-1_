# NOTE name need to be Dockerfile
FROM python:3.9

RUN pip install mysql-connector-python

# Install PyJWT
RUN pip install PyJWT

WORKDIR /usr/app/src

# Make port 8080 available to the world outside this container
EXPOSE 8010


COPY app.py ./
COPY user_service.py ./
