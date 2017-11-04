# Monthly Journal 1

## The Idea
After toying with a few initial ideas, I talked to our in house security team because I wanted to a real world security related problem for my project. After a quick chat, a good idea came about. A file integrity monitoring solution, or FIM. I had to do a little research. Turns out, there are many tools already that do something similar. Tripwire, Aide, Samhain to name a few. Almost all qre built in C derivatives for obvious performance reasons. My plan is to write an application which addresses the specific uses cases and requirements and develop with a modern programing language and using existing PAAS, libraries and services as much as possible.

## RWE

The treat of ransom-ware is very much to the forefront of Watson Platform for Health security concerns. Patient Health Information (PHI) is highly valued by cyber criminals and our in-house Ops and Security team are engaged in a continuous cycle of security evaluation and improvement. The threat of malware inside the firewall is almost of grave concern and the potential for PHI loss if very real. We recognised the need for an IDS solution that can detect malware and Trojans and also detect and prevent a ransom-ware attack e.g. CryptoLocker[1] which typically involves encryption of victim's files.

## Getting Started

Trying to get started has been difficult due to work commitments.

![](assets/orig-design.png)

## Design & Requirements

My design centres on a client-server architecture using a master and slave approach. Any number of Slaves can be deployed on a server to monitor files and send back integrity information to the master which Compares integrity information with that stored in a secure database to ensure the integrity of monitored files.

## Python

I have decided to use Python to develop my solution due to the flexibility of the language and the speed at which results can be achieved. Python also offers a huge array of community supported libraries and functions that I hope to be able to take advantage of. Python also has numerous web frameworks. I am going to utilise the Flask framework for my application using a micro-services approach. Flask is also supported by Bluemix which is where I plan to host my Python application. I have very little practical experience with Python.

## Bluemix

Bluemix is a great platform for learning new technologies. It supports Flask web frameworks and has a number of different data storage solutions. I chose Cloudant because I want to get more hands on with NOSQL and I already have a lot of experience with DB2.

## Containers

Spent most of the time this week trying to containerise the application. I'm heavily invested in DevOps in my day job so I've played a bit Docker and regularly attend meetups. Before the app can be deploy on the Watson platform, it will need to run in a container. Time spent getting everything working could probably have been spent on other features but once I start on something, I can't leave it alone.

`docker build -t alanoneill/pyfim:latest . `

```docker
FROM ubuntu:latest
MAINTAINER "alan.oneill75@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV SLACKTOKEN=xoxp-263593032944-263593033264-263845823617-77037eade80a620aded289030641096d
#ENTRYPOINT ["python"]
#CMD ["app.py"]
CMD ["python","-u","app.py"]
```

## Kubernetes

I've become obsessed with Kubernetes lately. I first became aware of it watching a Google Dev conference on YouTube a couple of years ago. It's really is amazing technology. Bluemix (soon to be known as IBM Cloud) offers a free one node cluster so of course I had to spend time getting the app deployed as a Kube service. In order to get the deployment to work on a Bluemix cluster, I needed to publish my image to [dockerhub](https://hub.docker.com/r/alanoneill/pyfim/).

```yaml
apiVersion: apps/v1beta1
kind: Deployment
metadata:
  name: pyfim-app
  labels:
    app: pyfim-app
spec:
  selector:
    matchLabels:
      app: pyfim-app
  template:
    metadata:
      labels:
        app: pyfim-app
    spec:
      containers:
      - name: pyfim-app
        image: alanoneill/pyfim
        ports:
        - containerPort: 5000
```

```yaml
apiVersion: v1
kind: Service
metadata:
  name: pyfim-service
  labels:
    name: pyfim-app
spec:
  type: NodePort
  ports:
    - port: 5000
      targetPort: 5000
      protocol: TCP
      name: pyfim-service
  selector:
    app: pyfim-app
```

[1] https://en.wikipedia.org/wiki/CryptoLocker
