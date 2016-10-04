#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
from setuptools import setup


pypi_desc = '''
Why a logstash / grok port to Python?
=====================================

I am not much into Ruby but I like the logstash approach to logfile parsing. So I want to use this in Python.

One solution would be to use the C version of logstash / grok (https://github.com/jordansissel/grok) and to write a wrapper:

* https://github.com/kiwi0530/python-grok
* https://github.com/emgee/libgrok-py

Basically grok assembles regular expressions. I already know that in Python file processing with regular expressions is blazingly fast so I choose to port it to Python. Since a grok package already exists in Python for something completely different I had to reverse engineer it. Thus **the name korg**.


Status
======

* Base functionality is implemented including tests
* Logstash patterns are included
* Some grok features are still missing (not sure which ones are really necessary)

I made some first benchmarks to verify whether my performance requirements can be realized with this approach. Please do not use this results in any blog posts or articles since this is not a complete benchmark (from a statistical view point the sample size is way too small).
'''

def find_pattern_files():
    return [os.path.join('patterns', file) for file in os.listdir('patterns')
        if re.match(r'^[\w-]+$', file)]

setup(
    url='http://www.finklabs.org/',
    author='Mark Fink',
    author_email='mark@finklabs.de',
    description='Fast logfile parsing. This is a port of Ruby logstash / grok to Python',
    long_description=pypi_desc,
    name='korg',
    version='0.0.6',
    packages=['korg'],
    data_files=[('patterns', find_pattern_files())],
    install_requires=['regex >= 2013-06-05'],
    license='MIT License',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
        'Topic :: System :: Systems Administration',
        'Natural Language :: English',
    ],
)
