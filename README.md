# KORG

[![Build Status](https://travis-ci.org/markfink/korg.svg?branch=master)](https://travis-ci.org/markfink/korg)
[![License](http://img.shields.io/badge/license-MIT-yellowgreen.svg)](MIT_LICENSE)

korg is the python port for the ruby logstash grok regular expression patterns.

## Quickstart

Logstash comes with over a 100 built in patterns for structuring unstructured data. You should definitely take advantage of this when you work with log data like like from apache, linux, haproxy, aws, and so forth. But you should also use it when working with unstructured data and you simply provide custom pattern yourself. 

In this demo I quickly show you how to use it on a simple webserver log sample:

``` text
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
127.0.0.1 - - [18/Jan/2020 10:28:19] "GET /index.html HTTP/1.1" 404 -
127.0.0.1 - - [18/Jan/2020 10:28:27] "GET /secret.txt HTTP/1.1" 200 -
...
```

Usually I start by putting a sample log line into [Grok Debugger](https://grokdebug.herokuapp.com/) and develop the pattern by using the logstash patterns (like what you would do using ruby logstash). Grok patterns are structured like this: %{NAME:IDENTIFIER}. NAME is the name of the logstash pattern you want to use, IDENTIFIER is the identifier you are giving to the matched text.

![webserver log pattern](https://raw.githubusercontent.com/markfink/korg/master/docs/media/grok_debugger.png)

Once the pattern works (should try out other log lines, too) we can automate this using korg.

``` python
>>> from korg import LineGrokker, PatternRepo
>>> 
>>> pr = PatternRepo()  # use the std. logstash grok patterns
>>> lg = LineGrokker('%{IPORHOST:clientip} - - %{SYSLOG5424SD} "(?:%{WORD:verb} %{NOTSPACE:request}(?: HTTP/%{NUMBER:httpversion})?|%{DATA:rawrequest})" %{NUMBER:response} (?:%{NUMBER:bytes}|-)', pr)
>>> 
>>> print(lg.grok('''127.0.0.1 - - [18/Jan/2020 10:28:27] "GET /secret.txt HTTP/1.1" 200 -'''))
{'clientip': '127.0.0.1', 'verb': 'GET', 'request': '/secret.txt', 'httpversion': '1.1', 'rawrequest': None, 'response': '200', 'bytes': None}
``` 


## Why a logstash / grok port to Python?

I like the logstash `grok` approach to logfile parsing. So I want to use this in Python.

One solution would be to use the C version of logstash / grok (https://github.com/jordansissel/grok) and to write a wrapper:

* https://github.com/kiwi0530/python-grok
* https://github.com/emgee/libgrok-py

Basically grok assembles regular expressions. I already know that in Python file processing with regular expressions is blazingly fast so I choose to directly port it to Python. 

The pattern files are updated from the logstash grok project:
https://github.com/logstash-plugins/logstash-patterns-core

A big thank you belongs to the logstash community for an awesome job maintaining the regex pattern files! 


## Resources

* http://jpmens.net/2012/08/06/my-logstash-and-graylog2-notes/
* http://grokdebug.herokuapp.com/
