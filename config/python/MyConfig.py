# -*- coding:utf-8 -*-
import os, configparser

class Config(object):
    def __init__(self, config_filename = "../config.cnf"):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result

'''
USE:

import MyConfig as cfg

conf = cfg.Config('./config.cnf')
mysql_conf = conf.get_content('mysql')
host = mysql_conf['host']
'''