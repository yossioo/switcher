import time
import switcher_parser
import logging

ON_ICON = "🟥"
OFF_ICON = "⬛️"
READY_ICON = "🟠"
THERMOSTAT_ON = "🔴"
THERMOSTAT_OFF = "⚫️"
ALL_SYMBOLS = "✅🟥🟧🟨🟩🟦🟪⬛️⬜️🟫🔴🟠🟡🟢🔵🟣⚫️⚪️🟤"


class Notifier:
    def __init__(self, f_notify, logger=None):
        self._f_notify = f_notify

        if logger is None:
            logger = logging.getLogger("Notifier")
            logger.setLevel(logging.DEBUG)
        self.logger = logger

        self._time_swich_on = None
        self._time_thermostat_on = None
        self._accumulated_j = 0
        self._last_update_time = None
        self._prev_data = switcher_parser.Data()

        self.logger.info("Notifier constucted")

    def notify(self, text):
        self._f_notify(text)
        self.logger.debug(text)

    def update(self, data: switcher_parser.Data):
        now = time.time()
        if data._power > 0 and self._last_update_time != None:
            diff = now - self._last_update_time
            self._accumulated_j += data._power * diff
        self._last_update_time = now
        if data._is_on != self._prev_data._is_on:
            icon = ON_ICON if data._is_on else OFF_ICON
            self.notify(f"{icon} Switch is **{data.status()}** now")
        if (
            self._prev_data._is_on
            and data._power > 0
            and self._time_thermostat_on is None
        ):
            self.notify("Thermostat is **ON** now")
            self._time_thermostat_on = time.time()
        if data._power == 0 and self._time_thermostat_on is not None:
            diff = now - self._time_thermostat_on
            self._time_thermostat_on = None
            self._last_update_time = None
            kwh = self._accumulated_j / 3600000
            self._accumulated_j = 0
            if data._is_on:
                self.notify(
                    f"f{READY_ICON} Termostat is **OFF** after {diff:.1f} sec. (~{kwh} KWh)\nYou can take shower now!",
                )
            else:
                self.notify(
                    f"{THERMOSTAT_OFF} Switch turned **OFF** after {diff:.1f} sec. (~{kwh} KWh)"
                )
        self.logger.debug(f"self._prev_data={self._prev_data}")
        self.logger.debug(f"data={data}")
        self.logger.debug(f"self._time_thermostat_on={self._time_thermostat_on}")
        self._prev_data = data
