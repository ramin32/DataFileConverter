import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class ConfigError(KeyError):
    pass

class ProcessorConfig(object):
    def __init__(self, config_file): 
        self.config_dict = yaml.load(config_file, Loader=Loader)

    def map_field(self, processor, field):
        try:
            return self.config_dict[processor.ID]['mapping'][field]
        except KeyError:
            return field

    def hierachy(self):
        try:
            return self.config_dict['hierachy']
        except (KeyError, TypeError):
            raise ConfigError('No hierachy defined!')

    def shareable_siblings(self, processor):
        try:
            return self.config_dict[processor.ID]['shareable_siblings'].split()
        except (KeyError, TypeError):
            raise ConfigError('No sharable_siblings defined!')


