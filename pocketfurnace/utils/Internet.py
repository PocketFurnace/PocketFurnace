import requests


class Internet:

    @staticmethod
    def get_url(url):
        response = requests.get(url)
        return response.text

    @staticmethod
    def get_ip():
        return Internet.get_url("http://api.ipify.org/")

    @staticmethod
    def simple_curl(url, data, headers={}):
        result = requests.post(url, data=data, headers=headers)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print("[Internet/Error]: There was a problem executing (simple_curl()): " + err.strerror)
