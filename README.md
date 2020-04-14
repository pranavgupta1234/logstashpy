logstashpy : python logging handlers for logstash with SSL/TLS support
------

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![image](https://img.shields.io/pypi/v/logstashpy.svg?label=logstashpy)](https://pypi.org/project/logstashpy/)
[![image](https://img.shields.io/pypi/pyversions/logstashpy.svg)](https://pypi.org/project/logstashpy/)
[![image](https://img.shields.io/github/issues/pranavgupta1234/logstashpy.svg)](https://github.com/pranavgupta1234/logstashpy/issues)
[![image](https://img.shields.io/github/issues-pr/pranavgupta1234/logstashpy.svg)](https://github.com/pranavgupta1234/logstashpy/pulls)


![image](./img/logstashpy_noback.png)

This repository is inspired from original project [python-logstash](https://github.com/vklochan/python-logstash) and lot of code and pending PR's are also 
integrated here as well, some of them like SSL/TLS support. Moreover it is planned to support more serialization formats
as supported in logstash codecs. Currently msgpack is integrated. 

Some old formatters are shipped but ELK stack now promotes use of ECS. Check out [ecs-logging](https://github.com/elastic/ecs-logging-python)
for latest update. For all handlers default formatter is now StdlibFormatter from ecs_logging but you can always chose 
some other formatter or the old formatters.

Currently no class is exposed with ``__all__``under ``__init__.py`` for now as API might change in future. 

Installation
------------

To install logstashpy, simply use all time favorite pip and type :

``` {.sourceCode .bash}
$ pip install logstashpy
```

Usage
------

``` {.sourceCode .python}
>>> from logstash.handlers.tcp_handler import TCPLogstashHandler
>>> from ecs.logger 
>>> host = 'localhost'
>>> logger = logging.getLogger(__name__)
>>> logger.setLevel(logging.INFO)
>>> handler = TCPLogstashHandler(host, 5959, ssl=False, serializer='msgpack')
>>> logger.addHandler(handler)

>>> # add extra field to logstash message
>>> extra = {
>>>     'test_string': 'python version: ' + repr(sys.version_info),
>>>     'test_boolean': True,
>>>     'test_dict': {'a': 1, 'b': 'c'},
>>>     'test_float': 1.23,
>>>     'test_integer': 123,
>>>     'test_list': [1, 2, '3'],
>>> }
>>> logger.info('python-logstash: test extra fields', extra=extra)

```

SSL/TLS Support
------
SSL is enabled by default. To disable pass ``ssl=False`` in Handler's constructor.

To quickly setup SSL/TLS related certificates follow some commands below:

Generate certificates for Certificate Authority (for self signed certificates) 

Generate CA key (kind of like private key for CA, will prompt for password, keep it safe)
```
openssl genrsa -des3 -out localCA.key 2048
```
Generate CA pem file (kind of like public key for CA)
```
openssl req -x509 -new -nodes -key localCA.key -sha256 -days 1024 -out localCA.pem
```
Now we have a local certificate authority ready to sign some certificates.

Lets generate some private key along with CSR (Certificate Signing Request) for our local logstash server
which will be signed by our local certificate authority. You can pass some other configs here but left for simplicity.
```
openssl req -new -sha256 -nodes -out logserver.csr -newkey rsa:2048 -keyout logserver.key
```
Let's submit our CSR to our local CA and get out certificate (as protected, you will be prompted for the password as set before)
```
openssl x509 -req -in server.csr -CA localCA.pem -CAkey localCA.key -CAcreateserial -out logserver.crt -days 1000 -sha256
```
You will get a logserver.crt which logstash server can present to its clients valid for 1000 days.


Python Version Support
------

logstashpy supports python3


Sample Logstash Configuration
-----------------

Example Logstash Configuration (``logstash.conf``) for Receiving Events from logstashpy via TCP (omit ssl 
 related fields if not required):
```
input {
  tcp {
    port => 5959
    codec => json
    ssl_enable => true
    ssl_cert => "/path/to/server.crt"
    ssl_key => "/path/to/server.key"
    ssl_verify => false
  }
}
output {
   stdout {
     codec => rubydebug
   }
}
```

Documentation
-------------

Coming Soon.
