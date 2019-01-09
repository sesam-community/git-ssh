FROM python:3-alpine
MAINTAINER Baard H. Rehn Johansen "baard.johansen@sesam.io"

COPY ./service /service

RUN apk update
RUN apk add git
RUN apk add openssh

RUN pip install --upgrade pip

RUN pip install -r /service/requirements.txt

EXPOSE 5000/tcp
ENTRYPOINT ["python"]
CMD ["./service/service.py"]

