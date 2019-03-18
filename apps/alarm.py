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

class AlarmService(hass.Hass):

    def initialize(self):

        self.log("Started Alarm service")
        self.listen_state(self.check_time, "sensor.time")

        self.alarm_minutes = 30
        self.alarm_on_minutes = 0

        self.current_brightness = 0
        self.target_brightness = 255
        self.brightness_step = 255 / float(self.alarm_minutes)

        wakeup_time_input = self.args['wakeup_time']
        current_wakeup_time = self.get_state(wakeup_time_input)
        self.set_state(wakeup_time_input, state=current_wakeup_time)
        self.listen_state(self.set_alarm, self.args['wakeup_time'])

    def set_alarm(self, entity, attribute, old, new, kwargs):
        try:
            self.wakeup_time = parse(new)
            self.alarm_start = self.wakeup_time - relativedelta(minutes=self.alarm_minutes)
            self.log('Alarm starting at {} so you wake up at {}'.format(self.alarm_start, self.wakeup_time))
        except ValueError:
            self.log('Alarm time is invalid!')

    def check_time(self, entity, attribute, old, new, kwargs):
        current_time = parse(new)

        self.log('{} {} {}'.format(current_time, self.alarm_start, self.wakeup_time))
        if self.alarm_start is not None and current_time >= self.alarm_start:
            self.log('Starting wake up')
            self.start_alarm()
            self.current_brightness += self.brightness_step

    def start_alarm(self):
        self.turn_on('light.jani_s_room', brightness=self.current_brightness, color_temp=1)
