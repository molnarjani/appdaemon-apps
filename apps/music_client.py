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
        self.data = {"jsonrpc": "2.0", "id": 1, "method": self.method, "params": self.params}

    def _send_command(self):
        response = requests.post('http://127.0.0.1:6680/mopidy/rpc', headers=self.headers, data=self.data)
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
        return response
