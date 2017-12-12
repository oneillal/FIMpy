FROM ubuntu:zesty
MAINTAINER "alan.oneill75@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential libldap2-dev libsasl2-dev libssl-dev
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=0
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
EXPOSE 5000
ENV SLACKTOKEN=xoxp-263593032944-263593033264-285370171619-af047513158f7673de13a587fad919b3
#ENTRYPOINT ["python"]
#CMD ["main.py"]
CMD ["python","-u","main.py","--alert","--auto"]
