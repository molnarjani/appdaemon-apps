import json
import requests


class MusicClient(object):
    """ Controls MPD service via jsonrpc """

    def __init__(self, url):
        self.url = url
        self.headers = {
            'Content-Type': 'application/json',
        }

    def _send_command(self, method='', params={}):
        self.data = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data))
        return response.json()

    @property
    def is_playing(self):
        response = self._send_command('core.playback.get_state')
        return response['result'] == 'playing'

    def start(self):
        return self._send_command('core.playback.play')

    def stop(self):
        return self._send_command('core.playback.stop')

    def get_volume(self):
        response = self._send_command('core.mixer.get_volume')
        return response['result']

    def set_volume(self, volume):
        return self._send_command('core.mixer.set_volume', {'volume': volume})
