#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extension for AppLoader
"""

import os
from celery.loaders.app import AppLoader
from celery.utils.log import get_logger


__all__ = ['AppExLoader']

logger = get_logger(__name__)


class AppExLoader(AppLoader):
    """
    Extension for AppLoader
    1. add configuration file read
    """

    @staticmethod
    def _read_config_file(name):
        from celery_ex.config import Config
        try:
            conf = Config(name)
            celery_conf = conf.pop("celery")
            if celery_conf:
                for key, value in celery_conf.items():
                    conf.update(key, value)
        except FileExistsError:
            logger.error("cson config file is not exist : %s", name)
            print("cson config file is not exist : {0}".format(name))
            return {}
        else:
            return conf()

    def read_configuration(self, env='CELERY_CONFIG_MODULE'):
        custom_config = os.environ.get(env)
        if custom_config:
            if custom_config.endswith('.cson') or custom_config.endswith('.json'):
                conf = self._read_config_file(custom_config)
                print(conf)
                return conf
            else:
                return super(AppExLoader, self).read_configuration(env=env)
        return {}
