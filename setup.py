#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
#from distutils.core import setup
from setuptools import setup


def find_pattern_files():
    return [os.path.join('patterns', file) for file in os.listdir('patterns')
        if re.match(r'^[\w-]+$', file)]

setup(
    author='Mark Fink',
    author_email='mark@mark-fink.de',
    description='Fast logfile parsing. This is a port of Ruby logstash / grok to Python',
    long_description=open('README.md').read(),
    url='https://github.com/aogaeru/korg',
    name='korg',
    version='0.0.3',
    packages=['korg'],
    data_files=[('patterns', find_pattern_files()), 'README.md'],
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
