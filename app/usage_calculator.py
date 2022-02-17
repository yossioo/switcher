import time

from switcher_parser import SwitcherData


class UsageCalculator:
    def __init__(self):
        self._accumulated_j = 0
        self._latest_data = SwitcherData()
        self._latest_update_time = time.time()
    
    def update_data(self, data: SwitcherData):
        now = time.time()
        ## TODO: Calculate usage
        ## TODO: notify on state change: main switch and thermostat
        ## TODO: notify usage on main switch off / thermostat off

        self._latest_update_time = now
