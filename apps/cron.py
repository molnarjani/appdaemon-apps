from datetime import datetime
import appdaemon.plugins.hass.hassapi as hass
from juice.main import Juice

class CronService(hass.Hass):
    """ Cron service to run scheduled tasks """

    def initialize(self, *args, **kwargs):
        self.run_daily(self.fetch_savings, datetime(2019, 5, 31, 21, 53), 1, **kwargs)

    def fetch_savings(self, *args, **kwargs):
        self.log('I ran')
        Juice().execute()


