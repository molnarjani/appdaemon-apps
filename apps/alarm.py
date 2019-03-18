import appdaemon.plugins.hass.hassapi as hass

#
# Alarm App
#
# Args:
#   - alarm_time: time you want to wake up at
#   - light_id: light to trigger
#
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime

class AlarmService(hass.Hass):

    def initialize(self):

        self.log("Started Alarm service")
        self.run_every(self.check_time, datetime.now(), 1)

        self.alarm_minutes = 30
        self.alarm_on_minutes = 0

        self.current_brightness = 0
        self.target_brightness = 255
        self.brightness_step = 255 / float(self.alarm_minutes)

        self.listen_state(self.set_alarm, self.args['wakeup_time'])

    def set_alarm(self, entity, attribute, old, new, kwargs):
        try:
            self.wakeup_time = parse(new)
            self.alarm_start = self.wakeup_time - relativedelta(minutes=self.alarm_minutes)
        except ValueError:
            self.log('Alarm time is invalid!')

    def check_time(self, entity, attribute, old, new, kwargs):
        print(self, entity, attribute, old, new, kwargs)

        current_time = parse(new)

        self.log('{} {} {}'.format(current_time, self.alarm_start, self.wakeup_time))
        if self.alarm_start is not None and current_time >= self.alarm_start:
            self.log('Starting wake up')
            self.start_alarm()
            self.current_brightness += self.brightness_step

    def start_alarm(self):
        self.turn_on('light.jani_s_room', brightness=self.current_brightness, color_temp=1)
