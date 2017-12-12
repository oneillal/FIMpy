## Containers

Spent most of the time this week trying to containerise the application. I'm heavily invested in DevOps in my day job so I've played a bit Docker and regularly attend meetups. Before the app can be deploy on the Watson platform, it will need to run in a container. Time spent getting everything working could probably have been spent on other features but once I start on something, I can't leave it alone.

`$ docker build -t alanoneill/fimpy:latest . `

```docker
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
ENV SLACKTOKEN=xoxp-263593032944-263593033264-276857887971-9e6816582c04cae19fb0f6f6f6287e21
#ENTRYPOINT ["python"]
#CMD ["main.py"]
CMD ["python","-u","main.py","--alert","--auto"]
```
