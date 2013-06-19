Why a logstash / grok port to Python
====================================

I am not into Ruby but I like the logstash approach to logfile parsing.

One approach would be to use the C version of grok (https://github.com/jordansissel/grok) and to write a wrapper:

https://github.com/kiwi0530/python-grok
https://github.com/emgee/libgrok-py

Based on the functionality that grok provides I choose to port it to Python. I hope that korg is very fast but that is not yet proven.


Status
======

* Base functionality is implemented including tests
* Logstash patterns are included
* Many grok features are still missing


Resources
=========

http://jpmens.net/2012/08/06/my-logstash-and-graylog2-notes/
http://grokdebug.herokuapp.com/
