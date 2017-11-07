## SSL

I'm pretty use to SSL, PKI and the like but being new to Python, I need to do a little research. Turns out that getting SSL up and running in Python is a doddle (like most things). Found a great little snippet [here](http://flask.pocoo.org/snippets/111/) and a good tutorial [here](http://bobthegnome.blogspot.co.uk/2007/08/making-ssl-connection-in-python.html).


I generate a self-signed cert and literally 5 minutes later I had TLS 1.2 AES256 secure communication with Elliptic-curve Diffie–Hellman no less! Of course it's not 100% secure because it's not CA signed and I did spend consider using LetsEncrypt to get a free CA signed cert but then I figure it was only a nice to have.

Booya!

```bash
$ curl -v -k --url https://127.0.0.1:5000/api/fimpy
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
* ALPN, offering http/1.1
* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
* successfully set certificate verify locations:
*   CAfile: /etc/ssl/certs/ca-certificates.crt
  CApath: /etc/ssl/certs
* TLSv1.2 (OUT), TLS header, Certificate Status (22):
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS change cipher, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
```


