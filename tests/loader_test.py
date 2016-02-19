#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
from celery_ex.loader import AppExLoader
# from celery.tests.case import AppCase


TEST_CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_config.cson")


class AppExLoaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_read_config(self):
        os.environ["TEST_APP_EX_LOADER_CONFIG"] = TEST_CONFIG
        loader = AppExLoader(None)
        conf = loader.read_configuration("TEST_APP_EX_LOADER_CONFIG")
        self.assertEqual(conf["BROKER_URL"], "redis://localhost:6379/1")

    def test_read_config_defalut(self):
        os.environ["CELERY_CONFIG_MODULE"] = TEST_CONFIG
        loader = AppExLoader(None)
        self.assertEqual(loader.conf["BROKER_URL"], "redis://localhost:6379/1")


if __name__ == '__main__':
    unittest.main()
