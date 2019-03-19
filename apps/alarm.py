import appdaemon.plugins.hass.hassapi as hass

# Alarm App
#
# Args:
#   - wakeup_time: time you want to wake up at
import json
import requests

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

class MusicService(object):
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


class AlarmService(hass.Hass):

    def initialize(self):

        self.log("Started Alarm service")
        self.listen_state(self.check_time, "sensor.time")

        self.alarm_minutes = 45
        self.alarm_on_minutes = 0

        self.current_brightness = 0
        self.target_brightness = 255
        self.brightness_step = 255 / float(self.alarm_minutes)

        wakeup_time_input = self.args['wakeup_time']
        current_wakeup_time = self.get_state(wakeup_time_input)
        # Initialize alarm
        self.set_alarm(wakeup_time_input, 'value', None, current_wakeup_time, {})

        self.listen_state(self.set_alarm, self.args['wakeup_time'])

    def set_alarm(self, entity, attribute, old, new, kwargs):
        self.log("set_alarm: {}".format(new))
        try:
            self.wakeup_time = parse(new)
            self.alarm_start = self.wakeup_time - relativedelta(minutes=self.alarm_minutes)
            self.log('Alarm starting at {} so you wake up at {}'.format(self.alarm_start.time(), self.wakeup_time.time()))
        except ValueError:
            self.log('Alarm time is invalid!')

    def check_time(self, entity, attribute, old, new, kwargs):
        current_time = parse(new)
        self.log('Current time: {}'.format(current_time.time()))

        if self.alarm_start is not None and self.alarm_start.time() <= current_time.time() <= self.wakeup_time.time():
            self.log('Starting wake up')
            self.start_alarm()
            self.current_brightness += self.brightness_step

    def start_alarm(self):
        self.turn_on('light.jani_s_room', brightness=self.current_brightness, color_temp=1)
