import platform
import subprocess


class Utils:

    @staticmethod
    def get_os():
        return platform.system()

    @staticmethod
    def getMachineUniqueId():
        return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
