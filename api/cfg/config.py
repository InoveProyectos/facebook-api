# !/usr/bin/env python

from configparser import ConfigParser

def config(section, filename='config.ini'):
    # Read config file
    parser = ConfigParser()
    parser.read(filename)

    # Read section
    config_param = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config_param[param[0]] = param[1] # Assign each key its corresponding value
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return config_param
