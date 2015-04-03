import re


def valid_app_name(name):
    return re.match('^[a-z0-9-]{1,12}$', name) is not None


def safepath(path):
    return '..' not in path and not path.strip().startswith('/')
