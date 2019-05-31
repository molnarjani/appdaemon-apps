from datetime import datetime
import appdaemon.plugins.hass.hassapi as hass
from juice.main import Juice

class CronService(hass.Hass):
    """ Cron service to run scheduled tasks """

    def initialize(self, *args, **kwargs):
        self.run_minutely(self.fetch_savings, datetime.datetime(2019, 05, 31, 21, 45), 1, **kwargs)

    def fetch_savings(self, *args, **kwargs):
        Juice().execute()


