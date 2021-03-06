from datetime import time
import appdaemon.plugins.hass.hassapi as hass
from juice.main import Juice

class CronService(hass.Hass):
    """ Cron service to run scheduled tasks """

    def initialize(self, *args, **kwargs):
        self.run_daily(self.fetch_savings, time(20, 00), **kwargs)

    def fetch_savings(self, *args, **kwargs):
        self.log('Fetching savings...')
        Juice().execute()
        self.log('Savings fetched!')


