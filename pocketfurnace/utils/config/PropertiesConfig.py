import configparser
import os


class PropertiesConfig:
    path = None

    def __init__(self, config_path):
        self.path = config_path
        if not os.path.isfile(config_path):
            file = open(config_path, 'w')
            file.write("")
            file.close()

    def getFloat(self, section, key) -> float:
        config = configparser.RawConfigParser()
        config.read(self.path)
        return config.getfloat(section, key)

    def getInt(self, section, key) -> int:
        config = configparser.RawConfigParser()
        config.read(self.path)
        return config.getint(section, key)

    def getBoolean(self, section, key) -> bool:
        config = configparser.RawConfigParser()
        config.read(self.path)
        return config.getboolean(section, key)

    def getString(self, section, key) -> str:
        config = configparser.RawConfigParser()
        config.read(self.path)
        return config.get(section, key)

    def set(self, section, key, value):
        config = configparser.RawConfigParser()
        config.add_section(section)
        config.read(self.path)
        config.set(section, key, value)
        with open(self.path, 'w') as file:
            config.write(file)
            file.close()

    def remove_section(self, section):
        config = configparser.RawConfigParser()
        config.read(self.path)
        config.remove_section(section)
        with open(self.path, 'w') as file:
            config.write(file)
            file.close()

    def remove_option(self, section, key):
        config = configparser.RawConfigParser()
        config.read(self.path)
        config.remove_option(section, key)
        with open(self.path, 'w') as file:
            config.write(file)
            file.close()