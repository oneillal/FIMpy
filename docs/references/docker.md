# Docker Reference

### Building the FIMpy Image

```bash
~/dev/project/FIMpy/app(master*) » docker build -t alanoneill/fimpy:latest .
Sending build context to Docker daemon  71.17kB
Step 1/10 : FROM ubuntu:zesty
 ---> 5e9fde03a0de
Step 2/10 : MAINTAINER "alan.oneill75@gmail.com"
 ---> Using cache
 ---> 5914a7f13422
Step 3/10 : RUN apt-get update -y
 ---> Using cache
 ---> e5f757b323dc
Step 4/10 : RUN apt-get install -y python-pip python-dev build-essential libldap2-dev libsasl2-dev libssl-dev
 ---> Using cache
 ---> 814066000105
Step 5/10 : COPY . /app
 ---> Using cache
 ---> 56cdbebdee06
Step 6/10 : WORKDIR /app
 ---> Using cache
 ---> 8ff32a4630b2
Step 7/10 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> 0c9d470d64cf
Step 8/10 : EXPOSE 5000
 ---> Using cache
 ---> 725ca2626d92
Step 9/10 : ENV SLACKTOKEN
 ---> Using cache
 ---> 0e559213ef1e
Step 10/10 : CMD python -u main.py
 ---> Using cache
 ---> a052e2fe335b
Successfully built a052e2fe335b
Successfully tagged alanoneill/fimpy:latest
```

### Starting a FIMpy Container

```bash
~/dev/project/FIMpy/app(master*) » docker run -d -p 5000:5000 --name fimpy alanoneill/fimpy
21a02c2de547b0957f1ac1a9ac0cc69b983ed8b29fa4f1a5a2b2a0c0ca368158
```

### Push to DockerHub

```bash
~/dev/project/FIMpy/app(master*) » docker push alanoneill/fimpy
The push refers to a repository [docker.io/alanoneill/fimpy]
0bd94378fefa: Mounted from alanoneill/fimpy
5ac2b699e6fc: Mounted from alanoneill/fimpy
043f86434fa3: Mounted from alanoneill/fimpy
930be9908569: Mounted from alanoneill/fimpy
a5bfda07c31b: Mounted from alanoneill/fimpy
4cb653496843: Mounted from alanoneill/fimpy
69da000be6ed: Mounted from alanoneill/fimpy
3eaf555ee1db: Mounted from alanoneill/fimpy
71b5d87d106c: Mounted from alanoneill/fimpy
latest: digest: sha256:abde77d42f93270b12836181baae8615298229bc4a9aa2359997b70a0451bd06 size: 2203
```
