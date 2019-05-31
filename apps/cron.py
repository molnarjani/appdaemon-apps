from datetime import datetime
import appdaemon.plugins.hass.hassapi as hass
from juice.main import execute

class CronService(hass.Hass):
    """ Cron service to run scheduled tasks """

    def initialize(self, *args, **kwargs):
        self.run_minute(self.fetch_savings, datetime.now(), 1, **kwargs)

    def fetch_savings(self, *args, **kwargs):
        self.log('I ran')
        execute()


