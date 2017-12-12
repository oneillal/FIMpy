# ![](docs/assets/face-monkey.png)&nbsp;FIMpy - File Integrity Monitoring

Gitbook Documentation: https://oneillal.github.io/FIMpy


FIMpy is running at the following url for evaluation: https://173.193.85.141:30853/

## Process Flow

![](docs/assets/fimpy-process-flow.png)

Using curl as follows:

### POST /api/v1/baseline
```
» curl -v -k -w '\n' -X POST -u "vikas.sahni:Tb3q9KvuPtg#R&" --url https://173.193.85.141:30853/api/v1/baseline
*   Trying 173.193.85.141...
* TCP_NODELAY set
* Connected to 173.193.85.141 (173.193.85.141) port 30853 (#0)
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
* ALPN, server did not agree to a protocol
* Server certificate:
*  subject: C=IE; ST=DUB; L=Dublin; O=FIMpy; OU=FIMpy; CN=fimpy.io
*  start date: Dec  2 11:28:09 2017 GMT
*  expire date: Dec  2 11:28:09 2018 GMT
*  issuer: C=IE; ST=DUB; L=Dublin; O=FIMpy; OU=FIMpy; CN=fimpy.io
*  SSL certificate verify result: self signed certificate (18), continuing anyway.
* Server auth using Basic with user 'vikas.sahni'
> POST /api/v1/baseline HTTP/1.1
> Host: 173.193.85.141:30853
> Authorization: Basic dmlrYXMuc2Fobmk6VGIzcTlLdnVQdGcjUiY=
> User-Agent: curl/7.52.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json; charset=utf-8
< Content-Length: 889
< Server: Werkzeug/0.13 Python/2.7.13
< Date: Tue, 12 Dec 2017 23:45:59 GMT
<
{
  "docs": [
    {
      "createdate": 1513119531.3673096,
      "file": "/app/test/10kfile",
      "hash": "84ff92691f909a05b224e1c56abb4864f01b4f8e3c854e4bb4c7baf1d3f6d652",
      "hmac": "dc54a021fdb7e23b9bdf71c06383ffe792662054188c8eb0bb05a85f42877bf6",
      "host": "fimpy-app-3991716731-v14nt",
      "ipaddress": "172.30.91.249",
      "modifydate": 1513087888.0,
      "size": 10240,
      "status": 1,
      "type": "doc"
    },
    {
      "createdate": 1513119531.3673096,
      "file": "/app/test/20kfile",
      "hash": "cc61635da46b2c9974335ea37e0b5fd660a5c8a42a89b271fa7ec2ac4b8b26f6",
      "hmac": "f1999ee1223cb36f4fb64e12fc14a9d7596de34f73b8a1306e1f19a249afee2a",
      "host": "fimpy-app-3991716731-v14nt",
      "ipaddress": "172.30.91.249",
      "modifydate": 1513087909.0,
      "size": 20480,
      "status": 1,
      "type": "doc"
    }
  ]
* Curl_http_done: called premature == 0
* Closing connection 0
* TLSv1.2 (OUT), TLS alert, Client hello (1):
}
```

### GET /api/v1/baseline
```
» curl -v -k -w '\n' -u "vikas.sahni:Tb3q9KvuPtg#R&" --url https://173.193.85.141:30853/api/v1/baseline
*   Trying 173.193.85.141...
* TCP_NODELAY set
* Connected to 173.193.85.141 (173.193.85.141) port 30853 (#0)
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
* ALPN, server did not agree to a protocol
* Server certificate:
*  subject: C=IE; ST=DUB; L=Dublin; O=FIMpy; OU=FIMpy; CN=fimpy.io
*  start date: Dec  2 11:28:09 2017 GMT
*  expire date: Dec  2 11:28:09 2018 GMT
*  issuer: C=IE; ST=DUB; L=Dublin; O=FIMpy; OU=FIMpy; CN=fimpy.io
*  SSL certificate verify result: self signed certificate (18), continuing anyway.
* Server auth using Basic with user 'vikas.sahni'
> GET /api/v1/baseline HTTP/1.1
> Host: 173.193.85.141:30853
> Authorization: Basic dmlrYXMuc2Fobmk6VGIzcTlLdnVQdGcjUiY=
> User-Agent: curl/7.52.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json; charset=utf-8
< Content-Length: 845
< Server: Werkzeug/0.13 Python/2.7.13
< Date: Tue, 12 Dec 2017 23:47:05 GMT
<
{
  "docs": [
    {
      "createdate": 1513119531.3673096,
      "file": "/app/test/10kfile",
      "hash": "84ff92691f909a05b224e1c56abb4864f01b4f8e3c854e4bb4c7baf1d3f6d652",
      "hmac": "dc54a021fdb7e23b9bdf71c06383ffe792662054188c8eb0bb05a85f42877bf6",
      "host": "fimpy-app-3991716731-v14nt",
      "ipaddress": "172.30.91.249",
      "modifydate": 1513087888.0,
      "size": 10240,
      "status": 2
    },
    {
      "createdate": 1513119531.3673096,
      "file": "/app/test/20kfile",
      "hash": "cc61635da46b2c9974335ea37e0b5fd660a5c8a42a89b271fa7ec2ac4b8b26f6",
      "hmac": "f1999ee1223cb36f4fb64e12fc14a9d7596de34f73b8a1306e1f19a249afee2a",
      "host": "fimpy-app-3991716731-v14nt",
      "ipaddress": "172.30.91.249",
      "modifydate": 1513087909.0,
      "size": 20480,
      "status": 2
    }
  ]
* Curl_http_done: called premature == 0
* Closing connection 0
* TLSv1.2 (OUT), TLS alert, Client hello (1):
}
```


### POST /api/v1/verify
```
» curl -k -w '\n' -X POST -u "vikas.sahni:Tb3q9KvuPtg#R&" --url https://173.193.85.141:30853/api/v1/verify
{
  "docs": [
    {
      "file": "/app/test/10kfile",
      "host": "fimpy-app-3991716731-v14nt",
      "ipaddress": "172.30.91.249",
      "status": 2
    },
    {
      "file": "/app/test/20kfile",
      "host": "fimpy-app-3991716731-v14nt",
      "ipaddress": "172.30.91.249",
      "status": 2
    }
  ]
}
```
