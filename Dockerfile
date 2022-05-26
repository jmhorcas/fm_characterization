FROM python:3.9-alpine
RUN apk update && apk add build-base linux-headers

ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD [ "/bin/sh", "docker_init.sh" ]
