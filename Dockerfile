FROM python:3.9-alpine
RUN apk update && apk add build-base linux-headers
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
