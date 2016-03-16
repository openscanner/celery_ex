#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
read cson/json config
"""

import os
import json
import cson

__all__ = ["Config"]


class Config(object):
    """
    config load/manage class
    """

    def __init__(self, file=None):
        self._config = dict()
        # config to option
        self._config2opt = dict()
        # config module/options
        self._opt = dict()
        # config files list
        self._files = list()

        if file:
            self.load(file)

    def __call__(self):
        return self._config

    def add(self, module, config=None, config2opt=None):
        if not isinstance(module, str):
            raise TypeError("module name should be string")

        if config is None:
            config = dict()

        if not isinstance(config, dict):
            raise TypeError("module config should be dictionary")

        # don't add same module twice
        if self._config.get(module) is None:
            self._config.update({module: config})

        if config2opt and (not self._config2opt.get(module)):
            if not isinstance(config2opt, dict):
                raise TypeError("config2opt should be dictionary")
            self._config2opt.update({module: config2opt})

        # make options
        self._make_module_options(module)
        return

    def update(self, module, config):
        self._config.update({module: config})

        # make options
        self._make_module_options(module)

    def get(self, module):
        return self._config.get(module)

    def pop(self, module):
        return self._config.pop(module, {})

    def get_opt(self, module):
        return self._opt.get(module)

    def _make_module_options(self, module):
        if not module:
            return None

        config2opts = self._config2opt.get(module)
        if not config2opts:
            return None

        config = self._config.get(module)
        if not config:
            return None

        options = []
        for key, value in config.items():
            c2o = config2opts.get(key)
            if c2o is not None:
                opt = c2o.make_opt(value)
                if isinstance(opt, list):
                    options.extend(opt)

        if len(options) > 0:
            self._opt.update({module: options})

    def _load_config(self, opened_file, parser=cson):
        opened_file.seek(0, 0)
        buffer = opened_file.read()
        try:
            config_value = parser.loads(buffer)
        except Exception as e:
            print(e)
            return

        if config_value is not None:
            # update or add config
            for key, val in config_value.items():
                config_val = self._config.get(key)
                if config_val is not None:
                    config_val.update(val)
                else:
                    self._config[key] = val

    @staticmethod
    def _get_config(opened_file, parser=cson, module=None):
        opened_file.seek(0, 0)
        buffer = opened_file.read()
        try:
            config_value = parser.loads(buffer)
        except Exception as e:
            print(e)
            return None

        # specific module
        if module:
            return config_value.get(module)

        # all config if file
        return config_value

    def _load_config_file(self, config_file_path, config_file_list):
        config_parser = json
        file_type = config_file_path.rsplit('.', 1)[-1]
        if file_type == 'cson':
            config_parser = cson

        # load config
        with open(config_file_path, 'rt') as config_file:
            config_files = self._get_config(config_file, parser=config_parser, module="config_files")
            if config_files:
                config_paths = config_files.get("paths")
                for sub_config_path in config_paths:
                    if not os.path.isabs(sub_config_path) and not os.path.isfile(sub_config_path):
                        sub_config_path = os.path.abspath(
                            os.path.join(os.path.dirname(config_file_path), sub_config_path))
                    self._load_config_file(sub_config_path, config_file_list)

                config_file_list.extend(config_paths)

            self._load_config(config_file, parser=config_parser)

    def load(self, config_file=""):
        """
        load config from config file
        :param config_file:
        :return:
        """
        config_file_list = []

        # check file
        if (not config_file) or (not os.path.exists(config_file)):
            print("config file:%s is not exist" % config_file)
            raise FileExistsError
        else:
            # load config from file
            config_file = os.path.abspath(config_file)
            self._load_config_file(config_file, config_file_list)
            config_file_list.extend("config_file")
            self._files = config_file_list

        # make tools options
        for module, _ in self._config.items():
            self._make_module_options(module)


# option
SHORT_OPT = 1
LONG_OPT = 2


class Config2opt:
    """
    configuration to tool option
    """

    def __init__(self, opt_name, with_arg=True, opt_type=SHORT_OPT):
        self.opt_name = opt_name
        self.with_arg = with_arg
        self.opt_type = opt_type

    def make_opt(self, config_value):
        """
        make command line option according config value
        :param config_value:
        :return:
        """
        if isinstance(self.with_arg, str):
            if not isinstance(config_value, str):
                if config_value:
                    return [self.opt_name]
                else:
                    return self.opt_name
            else:
                arg = self.opt_name + (self.with_arg % config_value)
                return [arg]

        if not self.with_arg:
            if config_value:
                return [self.opt_name]
            else:
                # remove it
                return self.opt_name

        if not isinstance(config_value, str):
            config_value = str(config_value)

        if self.opt_type is SHORT_OPT:
            return [self.opt_name, config_value]
        else:
            return [self.opt_name + "=" + config_value]
