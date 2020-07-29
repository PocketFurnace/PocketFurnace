from abc import ABC
from pocketfurnace.utils.config.BaseConfig import BaseConfig
import json
import os


class JsonConfig(BaseConfig, ABC):
    path = None
    content = None

    def __init__(self, config_path, data={}):
        self.path = config_path
        if os.path.isfile(config_path):
            with open(config_path, 'r') as file:
                self.content = json.loads(file.read())
                file.close()
        else:
            with open(config_path, 'w') as file:
                file.write(json.dumps(data))
                file.close()
            with open(config_path, 'r') as f:
                self.content = json.loads(f.read())
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
            file.write(json.dumps(self.content))
            file.close()

    def remove(self, key):
        if self.exists(key):
            self.content.pop(key)
            self.save()

    def exists(self, key) -> bool:
        if key in self.content:
            return True
        else:
            return False
