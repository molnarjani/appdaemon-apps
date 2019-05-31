import appdaemon.plugins.hass.hassapi as hass

class CronService(hass.Hass):
    """ Cron service to run scheduled tasks """

    def initialize(self, *args, **kwargs):
        self.run_minutely(self.fetch_savings, 1, **kwargs)

    def fetch_savings(self, *args, **kwargs):
        self.log('I ran')


