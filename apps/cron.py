from datetime import datetime
import appdaemon.plugins.hass.hassapi as hass

class CronService(hass.Hass):
    """ Cron service to run scheduled tasks """

    def initialize(self, *args, **kwargs):
        self.run_every(self.fetch_savings, datetime.now(), 1, **kwargs)

    def fetch_savings(self, *args, **kwargs):
        self.log('I ran')


