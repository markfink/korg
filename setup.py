# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from codecs import open
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', format='md', to='rst')
    long_description = long_description.replace('\r', '')  # YOU  NEED THIS LINE
except(IOError, ImportError):
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

# get the dependencies and installs
with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')


install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and
                    (not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if 'git+' not in x]


def find_pattern_files():
    return [os.path.join('patterns', file) for file in os.listdir('patterns')
            if re.match(r'^[\w-]+$', file)]


setup(
    name='korg',
    version='0.0.8',
    description='Fast logfile parsing. This is a port of Ruby logstash / grok to Python',
    long_description=long_description,
    license='MIT',
    url='https://github.com/finklabs/korg',
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*', 'patterns']),
    data_files=[('patterns', find_pattern_files())],
    include_package_data=True,
    author='glomex SRE Team',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='mark.fink@glomex.com',
    entry_points={
        'gcdt10': [
            'bundler=gcdt_bundler.bundler',
        ],
    }
)
