FROM ubuntu:zesty
MAINTAINER "alan.oneill75@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libldap2-dev libsasl2-dev libssl-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
EXPOSE 5000
ENV SLACKTOKEN=
#ENTRYPOINT ["python"]
#CMD ["main.py"]
CMD ["python","-u","main.py"]
