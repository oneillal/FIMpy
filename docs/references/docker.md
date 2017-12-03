# Docker Reference

### Building the FIMpy Image

```bash
~/dev/project/FIMpy/app(master*) » docker build -t alanoneill/fimpy:latest .       oneillal@xubuntu
Sending build context to Docker daemon  1.376MB
Step 1/12 : FROM ubuntu:zesty
 ---> 5e9fde03a0de
Step 2/12 : MAINTAINER "alan.oneill75@gmail.com"
 ---> Using cache
 ---> 5914a7f13422
Step 3/12 : RUN apt-get update -y
 ---> Using cache
 ---> e5f757b323dc
Step 4/12 : RUN apt-get install -y python-pip python-dev build-essential libldap2-dev libsasl2-dev libssl-dev
 ---> Using cache
 ---> 814066000105
Step 5/12 : COPY . /app
 ---> 3bdabe4b6e42
Step 6/12 : WORKDIR /app
 ---> 609fb51cea1a
Removing intermediate container 72dd27b152b1
Step 7/12 : RUN pip install -r requirements.txt
 ---> Running in 53650b470620
Collecting Flask==0.12.2 (from -r requirements.txt (line 1))
  Downloading Flask-0.12.2-py2.py3-none-any.whl (83kB)
Collecting cf-deployment-tracker==1.0.4 (from -r requirements.txt (line 2))
  Downloading cf_deployment_tracker-1.0.4-py2.py3-none-any.whl
Collecting cloudant==2.4.0 (from -r requirements.txt (line 3))
  Downloading cloudant-2.4.0-py2-none-any.whl (66kB)
Collecting slacker==0.9.60 (from -r requirements.txt (line 4))
  Downloading slacker-0.9.60.tar.gz
Collecting pyopenssl (from -r requirements.txt (line 5))
  Downloading pyOpenSSL-17.5.0-py2.py3-none-any.whl (53kB)
Collecting python-ldap==2.4.28 (from -r requirements.txt (line 6))
  Downloading python-ldap-2.4.28.tar.gz (125kB)
Collecting pytz (from -r requirements.txt (line 7))
  Downloading pytz-2017.3-py2.py3-none-any.whl (511kB)
Collecting apscheduler (from -r requirements.txt (line 8))
  Downloading APScheduler-3.4.0-py2.py3-none-any.whl (57kB)
Collecting click>=2.0 (from Flask==0.12.2->-r requirements.txt (line 1))
  Downloading click-6.7-py2.py3-none-any.whl (71kB)
Collecting Werkzeug>=0.7 (from Flask==0.12.2->-r requirements.txt (line 1))
  Downloading Werkzeug-0.12.2-py2.py3-none-any.whl (312kB)
Collecting Jinja2>=2.4 (from Flask==0.12.2->-r requirements.txt (line 1))
  Downloading Jinja2-2.10-py2.py3-none-any.whl (126kB)
Collecting itsdangerous>=0.21 (from Flask==0.12.2->-r requirements.txt (line 1))
  Downloading itsdangerous-0.24.tar.gz (46kB)
Collecting requests>=2 (from cf-deployment-tracker==1.0.4->-r requirements.txt (line 2))
  Downloading requests-2.18.4-py2.py3-none-any.whl (88kB)
Collecting cryptography>=2.1.4 (from pyopenssl->-r requirements.txt (line 5))
  Downloading cryptography-2.1.4-cp27-cp27mu-manylinux1_x86_64.whl (2.2MB)
Requirement already satisfied: six>=1.5.2 in /usr/lib/python2.7/dist-packages (from pyopenssl->-r requirements.txt (line 5))
Requirement already satisfied: setuptools in /usr/lib/python2.7/dist-packages (from python-ldap==2.4.28->-r requirements.txt (line 6))
Collecting funcsigs; python_version == "2.7" (from apscheduler->-r requirements.txt (line 8))
  Downloading funcsigs-1.0.2-py2.py3-none-any.whl
Collecting tzlocal>=1.2 (from apscheduler->-r requirements.txt (line 8))
  Downloading tzlocal-1.5.1.tar.gz
Collecting futures; python_version == "2.7" (from apscheduler->-r requirements.txt (line 8))
  Downloading futures-3.2.0-py2-none-any.whl
Collecting MarkupSafe>=0.23 (from Jinja2>=2.4->Flask==0.12.2->-r requirements.txt (line 1))
  Downloading MarkupSafe-1.0.tar.gz
Collecting chardet<3.1.0,>=3.0.2 (from requests>=2->cf-deployment-tracker==1.0.4->-r requirements.txt (line 2))
  Downloading chardet-3.0.4-py2.py3-none-any.whl (133kB)
Collecting certifi>=2017.4.17 (from requests>=2->cf-deployment-tracker==1.0.4->-r requirements.txt (line 2))
  Downloading certifi-2017.11.5-py2.py3-none-any.whl (330kB)
Collecting urllib3<1.23,>=1.21.1 (from requests>=2->cf-deployment-tracker==1.0.4->-r requirements.txt (line 2))
  Downloading urllib3-1.22-py2.py3-none-any.whl (132kB)
Collecting idna<2.7,>=2.5 (from requests>=2->cf-deployment-tracker==1.0.4->-r requirements.txt (line 2))
  Downloading idna-2.6-py2.py3-none-any.whl (56kB)
Collecting cffi>=1.7; platform_python_implementation != "PyPy" (from cryptography>=2.1.4->pyopenssl->-r requirements.txt (line 5))
  Downloading cffi-1.11.2-cp27-cp27mu-manylinux1_x86_64.whl (405kB)
Requirement already satisfied: enum34; python_version < "3" in /usr/lib/python2.7/dist-packages (from cryptography>=2.1.4->pyopenssl->-r requirements.txt (line 5))
Requirement already satisfied: ipaddress; python_version < "3" in /usr/lib/python2.7/dist-packages (from cryptography>=2.1.4->pyopenssl->-r requirements.txt (line 5))
Collecting asn1crypto>=0.21.0 (from cryptography>=2.1.4->pyopenssl->-r requirements.txt (line 5))
  Downloading asn1crypto-0.23.0-py2.py3-none-any.whl (99kB)
Collecting pycparser (from cffi>=1.7; platform_python_implementation != "PyPy"->cryptography>=2.1.4->pyopenssl->-r requirements.txt (line 5))
  Downloading pycparser-2.18.tar.gz (245kB)
Building wheels for collected packages: slacker, python-ldap, itsdangerous, tzlocal, MarkupSafe, pycparser
  Running setup.py bdist_wheel for slacker: started
  Running setup.py bdist_wheel for slacker: finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/57/61/2c/99406ad2141fdf3ede576acedad209a3b63b9674af56bbfa19
  Running setup.py bdist_wheel for python-ldap: started
  Running setup.py bdist_wheel for python-ldap: finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/fb/35/3a/620971eea137c1452e122f9aef8820cf5f8e0f1c0413d4c8e6
  Running setup.py bdist_wheel for itsdangerous: started
  Running setup.py bdist_wheel for itsdangerous: finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/fc/a8/66/24d655233c757e178d45dea2de22a04c6d92766abfb741129a
  Running setup.py bdist_wheel for tzlocal: started
  Running setup.py bdist_wheel for tzlocal: finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/7c/a1/5d/0f37ce6eb6eea391bd185f5747429a93519be115d007263bcf
  Running setup.py bdist_wheel for MarkupSafe: started
  Running setup.py bdist_wheel for MarkupSafe: finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/88/a7/30/e39a54a87bcbe25308fa3ca64e8ddc75d9b3e5afa21ee32d57
  Running setup.py bdist_wheel for pycparser: started
  Running setup.py bdist_wheel for pycparser: finished with status 'done'
  Stored in directory: /root/.cache/pip/wheels/95/14/9a/5e7b9024459d2a6600aaa64e0ba485325aff7a9ac7489db1b6
Successfully built slacker python-ldap itsdangerous tzlocal MarkupSafe pycparser
Installing collected packages: click, Werkzeug, MarkupSafe, Jinja2, itsdangerous, Flask, chardet, certifi, urllib3, idna, requests, cf-deployment-tracker, cloudant, slacker, pycparser, cffi, asn1crypto, cryptography, pyopenssl, python-ldap, pytz, funcsigs, tzlocal, futures, apscheduler
  Found existing installation: idna 2.2
    Not uninstalling idna at /usr/lib/python2.7/dist-packages, outside environment /usr
  Found existing installation: cryptography 1.7.1
    Not uninstalling cryptography at /usr/lib/python2.7/dist-packages, outside environment /usr
Successfully installed Flask-0.12.2 Jinja2-2.10 MarkupSafe-1.0 Werkzeug-0.12.2 apscheduler-3.4.0 asn1crypto-0.23.0 certifi-2017.11.5 cf-deployment-tracker-1.0.4 cffi-1.11.2 chardet-3.0.4 click-6.7 cloudant-2.4.0 cryptography-2.1.4 funcsigs-1.0.2 futures-3.2.0 idna-2.6 itsdangerous-0.24 pycparser-2.18 pyopenssl-17.5.0 python-ldap-2.4.28 pytz-2017.3 requests-2.18.4 slacker-0.9.60 tzlocal-1.5.1 urllib3-1.22
 ---> dee3dcf2cdd6
Removing intermediate container 53650b470620
Step 8/12 : ENV TZ Europe/Dublin
 ---> Running in 86516e5bbaf0
 ---> 8e5a9bc6b218
Removing intermediate container 86516e5bbaf0
Step 9/12 : RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
 ---> Running in a713a30f5653
 ---> 2b7d12c15bdd
Removing intermediate container a713a30f5653
Step 10/12 : EXPOSE 5000
 ---> Running in 9116dd7c5ee9
 ---> a584a9d72491
Removing intermediate container 9116dd7c5ee9
Step 11/12 : ENV SLACKTOKEN
 ---> Running in df11fb9e4046
 ---> 5742487bdabf
Removing intermediate container df11fb9e4046
Step 12/12 : CMD python -u main.py
 ---> Running in 8ba97f6b39ec
 ---> 03084ca8c992
Removing intermediate container 8ba97f6b39ec
Successfully built 03084ca8c992
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
