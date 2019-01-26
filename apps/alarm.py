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

        self.alarm_time = self.get_state(self.args['alarm_time'])
        self.listen_state(self.set_alarm, self.args['alarm_time'])

        #self.toggle_light()

    def set_alarm(self, entity, attribute, old, new, kwargs):
        try:
            self.alarm_time = parse(new).time()
            self.log('Alarm set to: {}'.format(self.alarm_time))
        except ValueError:
            self.log('Alarm time is invalid!')

    def check_time(self, entity, attribute, old, new, kwargs):
        current_time = parse(new).time()
        #self.log('Current time: {}, Alarm time: {}'.format(current_time, self.alarm_time))

        if current_time == self.alarm_time:
            self.log('Starting wake up')
            self.start_alarm()

    def start_alarm(self):
        self.turn_on('light.jani_s_room', brightness=225, color_temp=1)
