import json
import requests


class MusicClient(object):
    """ Controls MPD service via jsonrpc """

    def __init__(self, url):
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.params = {}
        self.method = ''

    def _send_command(self):
        self.data = {"jsonrpc": "2.0", "id": 1, "method": self.method, "params": self.params}
        print(self.data)
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
        return response.json()

    def start(self):
        self.method = 'core.playback.play'
        return self._send_command()

    def stop(self):
        self.method = 'core.playback.stop'
        return self._send_command()

    def get_volume(self):
        self.method = 'core.mixer.get_volume'
        response = self._send_command()
        return response['result']

    def set_volume(self, volume):
        self.method = 'core.mixer.get_volume'
        self.params = {'volume': volume}
        return self._send_command()
