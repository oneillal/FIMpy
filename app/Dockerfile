FROM ubuntu:latest
MAINTAINER "alan.oneill75@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV SLACKTOKEN=
#ENTRYPOINT ["python"]
#CMD ["app.py"]
CMD ["python","-u","app.py"]
