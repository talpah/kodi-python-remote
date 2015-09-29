import os

from xbmcjson import XBMC

__author__ = 'cosmin'


class Config:
    default_config = {
        "hostname": "localhost",
        "port": 80,
        "username": "xbmc",
        "password": "xbmc"
    }

    def __init__(self, config_file=None, **kwargs):
        self.__dict__ = self.default_config.copy()
        if config_file is not None:
            import yaml
            with open(config_file, 'r') as fp:
                config = yaml.load(fp)
                self.__dict__.update(config)
        self.__dict__.update(kwargs)

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            raise AttributeError(attr)
        return self.__dict__[attr]

    def __setattr__(self, attr, value):
        if attr not in self.default_config:
            raise AttributeError(attr)
        self.__dict__[attr] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        return self.__dict__.keys()


class Kodi(XBMC):
    def __init__(self):
        my_dir = os.path.dirname(os.path.realpath(__file__))
        config_file = None
        if os.path.isfile(os.path.join(my_dir, 'config.yml')):
            config_file = os.path.join(my_dir, 'config.yml')
        config = Config(config_file)

        super(Kodi, self).__init__("http://{hostname}:{port}/jsonrpc".format(**config),
                                   username=config.username,
                                   password=config.password)
