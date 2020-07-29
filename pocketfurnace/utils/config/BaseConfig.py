import abc


class BaseConfig(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass

    @abc.abstractmethod
    def save(self):
        pass

    @abc.abstractmethod
    def exists(self, key) -> bool:
        pass

    @abc.abstractmethod
    def remove(self, key):
        pass
