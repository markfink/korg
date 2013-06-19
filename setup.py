#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import distribute_setup
distribute_setup.use_setuptools()

try:
    from setuptools import setup, find_packages
    have_setuptools = True
except ImportError:
    from distutils.core import setup
    def find_packages():
        return [
            'korg',
        ]
    have_setuptools = False

def find_pattern_files():
    return [os.path.join('patterns', file) for file in os.listdir('patterns')
        if re.match(r'^[\w-]+$', file)]

requires = ['regex>=2013-06-05']

setup(
    author='Mark Fink',
    author_email='mark@mark-fink.de',
    description='Fast logfile parsing. This is a port of Ruby logstash / grok to Python',
    url='https://github.com/aogaeru/korg',
    download_url='http://pypi.python.org/pypi/korg',
    name='korg',
    version='0.0.1',
    packages=find_packages(),
    license='MIT License',
    long_description=open('README.md').read(),
    scripts=[],
    platforms='any',
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
    data_files=[('patterns', find_pattern_files())]
)
