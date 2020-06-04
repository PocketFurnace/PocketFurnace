
class NoDynamicFieldsTrait:

    def __throw(self, field: str):
        return RuntimeError(f"Cannot access dynamic field {field}: Dynamic field access on {self.__class__} is no longer supported")

    def __get(self, name):
        raise self.__throw(name)

    def __set(self, name, value):
        raise self.__throw(name)

    def __isset(self, name):
        raise self.__throw(name)

    def __unset(self, name):
        raise self.__throw(name)
