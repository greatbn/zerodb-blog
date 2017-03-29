#!/usr/bin/python
"""
Load Config File
"""
import ConfigParser


CONF_FILE = '/tmp/my-blog.conf'


def get_config():
    """
    Return config object
    """
    config = ConfigParser.RawConfigParser()
    config.read(CONF_FILE)
    return config


if __name__ == '__main__':
    CONF = get_config()
    print "GET LOG LEVEL CONFIG: " + CONF.get('logging', 'log_level')
