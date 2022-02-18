import time
import logging
from switcher_parser import SwitcherData


class UsageCalculator:
    def __init__(self):
        self._logger = logging.getLogger("UsageCalculator")
        self._accumulated_j = 0
        self._latest_data = SwitcherData()
        self._latest_update_time = time.time()
        self._latest_thermostat_on_time = None
        self.counting = False
        self.active_time = 0
        self.total_consumption_kwh = 0
    
    def update_data(self, data: SwitcherData):
        now = time.time()
        dt = now - self._latest_update_time

        if data.active() and self._latest_data.active():
            mean_power = 0.5 * (data._power + self._latest_data._power)
            self._accumulated_j += mean_power * dt

        if data.active() and not self._latest_data.active():
            self._logger.info("Thermostat is active now, starting to count")
            self.counting = True
            self._accumulated_j = 0
            self._latest_thermostat_on_time = now
            self._active_time = now - self._latest_thermostat_on_time
            self._total_consumption_kwh = self._accumulated_j / 3600000

        if not data.active() and self._latest_data.active():
            self._logger.info("Thermostat is inactive now, summing up")
            self.counting = False
            self._active_time = now - self._latest_thermostat_on_time
            self._total_consumption_kwh = self._accumulated_j / 3600000
            self._latest_thermostat_on_time = None

        ## TODO: Calculate usage
        ## TODO: notify on state change: main switch and thermostat
        ## TODO: notify usage on main switch off / thermostat off

        self._latest_update_time = now
