## HMAC

I must admit it took a while to get my head around HMAC. I watched a bunch of YouTube videos and even then it wasn't making a whole lot of sense. I mean it was easy to generate hmac's and hashes in my Python code using the [hashlib](https://docs.python.org/2/library/hashlib.html) [1] and [hmac](https://docs.python.org/2/library/hmac.html) [2] libraries. What didn't make sense to me was why I didn't always getting the same hmac for the same file? Turns out in the end it was an initialisation error but it took a while to figure it out. I wasn't reinitialising the hmac within a loop and so I was calculating a running HMAC for all the files I was monitoring.

With hmac and hashlib, you use the update() method because it's advisable to read a certain number of blocks at a time and not read the whole file on one go. So you need to create a new HMAC for each and every file.

```python
for file in glob.glob(os.path.join(path, '*')):
    if os.path.isfile(file):
        f = open(file, 'rb')
        try:
            sha256 = hashlib.sha256()
            digest = hmac.new('key', '', hashlib.sha256)
            while True:
                block = f.read(BUF_SIZE)
                if not block:
                    break
                digest.update(block)
                sha256.update(block)
        finally:
            f.close()
```

**[1]** [https://docs.python.org/2/library/hashlib.html](https://docs.python.org/2/library/hashlib.html)

**[2]** [https://docs.python.org/2/library/hmac.html](https://docs.python.org/2/library/hmac.html)