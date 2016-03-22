#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TODO: File Comment
"""

import os
import re
import sys
from setuptools import setup, find_packages

if sys.version_info < (2, 6):
    raise Exception('Celery 3.1 requires Python 2.6 or higher.')

# -*- Distribution Meta -*-

re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_vers = re.compile(r"^VERSION\s*=\s*'.*'")
re_doc = re.compile(r'^"""(.+?)"""')


def rq(s):
    return s.strip("\"'")


def add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, rq(attr_value)),)


def add_version(m):
    v = m.group().split("'")[1]
    return (('VERSION', v),)


def add_doc(m):
    return (('doc', m.groups()[0]),)


pats = {re_meta: add_default,
        re_vers: add_version,
        re_doc: add_doc}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'celery_ex/__init__.py')) as meta_fh:
    meta = {}
    for line in meta_fh:
        if line.strip() == '# -eof meta-':
            break
        for pattern, handler in pats.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))


def get_requirements():
    return open('requirements.txt').read().splitlines()


install_requires = get_requirements()

setup(
    name='celery_ex',
    version=meta['VERSION'],
    description='Celery Extension',
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    platforms=['any'],
    license='BSD',
    packages=find_packages(exclude=['tests', 'tests.*', 'example', 'example.*'], include=['celery_ex', 'celery_ex.*']),
    install_requires=install_requires,

    #    entry_points={
    #        'console_scripts': [
    #            'flower = flower.__main__:main',
    #        ],
    #        'celery.commands': [
    #            'flower = flower.command:FlowerCommand',
    #        ],
    #    },
)
