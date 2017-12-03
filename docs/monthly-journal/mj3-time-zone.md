# Time-Zones

Every so often I rebuild the latest code into a docker image and test it. Low and behold, I got an error after I added the scheduler for continuous scanning. Looks like it's related to the time-zone. Since my containers are running on Bluemix, I have no idea what the time-zone should be.

```bash
~/dev/project/FIMpy/app(master*) » docker logs fimpy                               oneillal@xubuntu
Traceback (most recent call last):
  File "main.py", line 67, in <module>
    cron = BackgroundScheduler(daemon=True)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/base.py", line 82, in __init__
    self.configure(gconfig, **options)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/base.py", line 121, in configure
    self._configure(config)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/background.py", line 29, in _configure
    super(BackgroundScheduler, self)._configure(config)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/base.py", line 689, in _configure
    self.timezone = astimezone(config.pop('timezone', None)) or get_localzone()
  File "/usr/local/lib/python2.7/dist-packages/tzlocal/unix.py", line 131, in get_localzone
    _cache_tz = _get_localzone()
  File "/usr/local/lib/python2.7/dist-packages/tzlocal/unix.py", line 125, in _get_localzone
    raise pytz.UnknownTimeZoneError('Can not find any timezone configuration')
pytz.exceptions.UnknownTimeZoneError: 'Can not find any timezone configuration'
Traceback (most recent call last):
  File "main.py", line 67, in <module>
    cron = BackgroundScheduler(daemon=True)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/base.py", line 82, in __init__
    self.configure(gconfig, **options)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/base.py", line 121, in configure
    self._configure(config)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/background.py", line 29, in _configure
    super(BackgroundScheduler, self)._configure(config)
  File "/usr/local/lib/python2.7/dist-packages/apscheduler/schedulers/base.py", line 689, in _configure
    self.timezone = astimezone(config.pop('timezone', None)) or get_localzone()
  File "/usr/local/lib/python2.7/dist-packages/tzlocal/unix.py", line 131, in get_localzone
    _cache_tz = _get_localzone()
  File "/usr/local/lib/python2.7/dist-packages/tzlocal/unix.py", line 125, in _get_localzone
    raise pytz.UnknownTimeZoneError('Can not find any timezone configuration')
pytz.exceptions.UnknownTimeZoneError: 'Can not find any timezone configuration'
```

So after much trawling, thankfully I found the answer on StackEchange. I thought it was a python issue but turns out I need to specifically set a time-zone within a docker container with the following commands in my docker file. Job done.

```yaml
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
```

https://serverfault.com/questions/683605/docker-container-time-timezone-will-not-reflect-changes