import binascii as ba


class SwitcherData:
    def __init__(
        self,
        is_on: bool = False,
        current: float = -1.0,
        power: int = -1,
        auto_shutdown: int = -1,
        time_auto_shutdown: int = -1,
    ):
        self.is_on = is_on
        self._current = current
        self._power = power
        self._auto_shutdown = auto_shutdown
        self._time_auto_shutdown = time_auto_shutdown

    def __str__(self):
        return f"Status: {'ON ' if self.is_on else 'OFF'} Current={self._current:.1f}A Power={self._power}W"
        # return f"Status: {'ON ' if self.is_on else 'OFF'} Current={self._current:.1f}A Power={self._power}W\tAS:{self._auto_shutdown} will shutdown in {self._time_auto_shutdown}"

    def on_duration(self):
        min, sec = divmod(self.on_for_sec(), 60)
        if min > 59:
            hour, min = divmod(min, 60)
            t = f"{hour:02d}:{min:02d}:{sec:02d}"
        else:
            t = f"{min:02d}:{sec:02d}"
        return t

    def on_for_sec(self):
        return self._auto_shutdown - self._time_auto_shutdown

    def status(self):
        return "ON" if self.is_on else "OFF"

    def active(self):
        return self._power > 0


def parse_data(raw_data: bytes):
    state = None
    current = None
    power = None

    data_str = ba.hexlify(raw_data).decode()
    if data_str[0:4] != "fef0" and len(raw_data) != 165:
        raise RuntimeWarning("[!] Not a switcher broadcast message!")
    b = data_str[270:278]
    power = int(b[2:4] + b[0:2], 16)
    current = float(power) / float(220)
    is_on = data_str[266:270] != "0000"

    b = data_str[310:318]
    auto_shutdown = int(b[6:8] + b[4:6] + b[2:4] + b[0:2], 16)

    b = data_str[294:302]
    time_auto_shutdown = int(b[6:8] + b[4:6] + b[2:4] + b[0:2], 16)

    return SwitcherData(is_on, current, power, auto_shutdown, time_auto_shutdown)
