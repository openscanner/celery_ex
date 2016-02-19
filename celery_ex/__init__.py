#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extension for Celery, used by 杭州网蛙科技有限公司
"""

from collections import namedtuple


version_info_t = namedtuple(
    'version_info_t', ('major', 'minor', 'micro', 'releaselevel', 'serial'),
)

SERIES = 'Demo'
VERSION = version_info_t(0, 0, 1, '', '')
__version__ = '{0.major}.{0.minor}.{0.micro}{0.releaselevel}'.format(VERSION)
__author__ = 'Wu Yadong'
__contact__ = 'wuyd@openscanner.cn'
__homepage__ = 'https://github.com/openscanner/celery_ex'
__all__ = [
    'version', '__version__',
]
VERSION_BANNER = '{0} ({1})'.format(__version__, SERIES)
