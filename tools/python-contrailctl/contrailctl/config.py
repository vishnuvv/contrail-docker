import ConfigParser
import ast
import re


def read_config(config_file):
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    return config


class Configurator(object):

    def __init__(self, master_config_file, param_map):
        """Prepare configuration dict in a form that can be passed to ansible as variables
        :param master_config_file: container specific master config file
        """
        self.master_config_file = master_config_file
        self.master_config = read_config(self.master_config_file)
        self.param_map = param_map

    @staticmethod
    def _eval(data):
        if re.match(r"^\[.*\]$", data) or re.match(r"^\{.*\}$", data):
            return ast.literal_eval(data)
        else:
            return data

    def map(self, config_dict):
        """
        :param config_dict: config dictionary to be populated, the system may have to get multiple instances of
        Configurator in which case this config_dict should not be overwritten, so it always get updated
        :return: loaded config_dict
        """
        for section in self.master_config.sections():
            for param, value in self.master_config.items(section):
                if param in self.param_map.get(section, {}):
                    config_dict.update({self.param_map[section][param]: self._eval(value)})
                else:
                    config_dict.update({"{}_{}".format(section.lower(), param): self._eval(value)})

        return config_dict