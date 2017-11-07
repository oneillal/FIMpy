## Testing

#### POST /api/fimpy - Write monitored file info to db {#post-apifimpy---write-monitored-file-info-to-db}
```bash
$ curl -k -X POST -u admin:password --url https://127.0.0.1:5000/api/fimpy
Records added to db
```

#### GET /api/fimpy - Read monitored file info from db {#get-apifimpy---read-monitored-file-info-from-db}
```bash
$ curl -k -u admin:password --url https://127.0.0.1:5000/api/fimpy
[
  "/app/test/11kfile",
  "/app/test/sniff.py",
  "/app/test/jumpcloud_test_utility.sh",
  "/app/test/10kfile"
]
```

#### LDAP Authentication Failure {#ldap-authenication-failure}
```bash
$ curl -v -k -u admin:badpw --url https://127.0.0.1:5000/api/fimpy/scan
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
* ALPN, server did not agree to a protocol
* Server certificate:
*  subject: C=IE; ST=DUB; L=Dublin; O=IBM; OU=Watson; CN=xubuntu
*  start date: Nov  2 19:44:48 2017 GMT
*  expire date: Nov  2 19:44:48 2018 GMT
*  issuer: C=IE; ST=DUB; L=Dublin; O=IBM; OU=Watson; CN=xubuntu
*  SSL certificate verify result: self signed certificate (18), continuing anyway.
* Server auth using Basic with user 'admin'
> GET /api/fimpy/scan HTTP/1.1
> Host: 127.0.0.1:5000
> Authorization: Basic YWRtaW46YmFkcHc=
> User-Agent: curl/7.52.1
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 401 UNAUTHORIZED
* Authentication problem. Ignoring this.
< WWW-Authenticate: Basic realm="Login Required"
< Content-Type: text/html; charset=utf-8
< Content-Length: 20
< Server: Werkzeug/0.12.2 Python/2.7.13
< Date: Sun, 05 Nov 2017 19:18:25 GMT
<
* Curl_http_done: called premature == 0
* Closing connection 0
* TLSv1.2 (OUT), TLS alert, Client hello (1):
Authenticaton failed
```