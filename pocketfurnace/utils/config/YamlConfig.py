from abc import ABC
import yaml
import os

from pocketfurnace.utils.config.BaseConfig import BaseConfig


class YamlConfig(BaseConfig, ABC):
    path = None
    content = None

    def __init__(self, config_path, data={}):
        self.path = config_path

        if os.path.isfile(config_path):
            with open(config_path) as file:
                self.content = yaml.load(file, Loader=yaml.FullLoader)
                file.close()
        else:
            with open(config_path, 'w') as file:
                yaml.dump(data, file)
                file.close()
            with open(config_path) as f:
                self.content = yaml.load(f, Loader=yaml.FullLoader)
                f.close()

    def get(self, key):
        if self.exists(key):
            return self.content[key]
        else:
            return None

    def set(self, key, value):
        self.content[key] = value

    def save(self):
        with open(self.path, 'w') as file:
            yaml.dump(self.content, file)
            file.close()

    def remove(self, key):
        if self.exists(key):
            self.content.pop(key)
            self.save()

    def exists(self, key):
        if key in self.content:
            return True
        else:
            return False
