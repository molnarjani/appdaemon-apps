import appdaemon.plugins.hass.hassapi as hass

# Alarm App
#
# Args:
#   - wakeup_time: time you want to wake up at
from math import ceil
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from music_client import MusicClient


class AlarmService(hass.Hass):
    """ Starts playing music and turns lights and volume up incrementally """

    def initialize(self):

        self.log("Started Alarm service")
        self.music_client = MusicClient('http://127.0.0.1:6680/mopidy/rpc')
        self.listen_state(self.check_time, "sensor.time")

        self.alarm_minutes = 30

        self.current_volume = 5
        self.current_brightness = 1
        self.target_brightness = 255

        max_volume_input = self.args['max_volume']
        self.max_volume = float(self.get_state(max_volume_input))

        self.brightness_step = ceil(self.target_brightness / float(self.alarm_minutes))
        self.volume_step = ceil(self.max_volume / float(self.alarm_minutes))

        wakeup_time_input = self.args['wakeup_time']
        current_wakeup_time = self.get_state(wakeup_time_input)

        is_enabled_input = self.args['is_enabled']
        self.is_enabled = self.get_state(is_enabled_input)


        # Initialize alarm
        self.set_alarm(wakeup_time_input, 'value', None, current_wakeup_time, {})

        self.listen_state(self.set_alarm, self.args['wakeup_time'])
        self.listen_state(self.set_enabled, self.args['is_enabled'])
        self.listen_state(self.set_max_volume, self.args['max_volume'])

    def set_enabled(self, entity, attribute, old, new, kwargs):
        self.is_enabled = new == 'on'
        self.log("set_enabled: {}".format(self.is_enabled))

        if not self.is_enabled:
            self.music_client.stop()

    def set_max_volume(self, entity, attribute, old, new, kwargs):
        self.max_volume = float(new)

        if self.currenct_volume > self.max_volume:
            self.music_client.set_volume(self.max_volume)

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
            self.current_volume += self.volume_step

    def start_alarm(self):
        if self.is_enabled:
            if not self.music_client.is_playing:
                self.music_client.start()

            self.music_client.set_volume(min(self.max_volume, self.current_volume))

            color_temp = max(1, self.target_brightness - self.current_brightness)
            self.log('max(1, {} - {})'.format(self.target_brightness, self.current_brightness))
            self.turn_on('light.jani_s_room', brightness=min(self.target_brightness, self.current_brightness), color_temp=color_temp)
