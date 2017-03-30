#!/usr/bin/python3
"""
Load Config File
"""
import configparser


CONF_FILE = './my-blog.conf'


def get_config():
    """
    Return config object
    """
    config = configparser.RawConfigParser()
    config.read(CONF_FILE)
    return config


if __name__ == '__main__':
    CONF = get_config()
    print ("GET LOG LEVEL CONFIG: %s" % CONF.get('logging', 'log_level'))
