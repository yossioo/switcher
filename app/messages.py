ON_ICON = "π₯"
OFF_ICON = "β¬οΈ"
READY_ICON = "π "
THERMOSTAT_ON = "π΄"
THERMOSTAT_OFF = "β«οΈ"

SHOWER1 = "π"
SHOWER2 = "πΏ"
ALL_SYMBOLS = """
βπΏπβ¨οΈβοΈ
ππ΄π π‘π’
π΅π£β«οΈβͺοΈπ€
π₯π§π¨π©π¦
πͺβ¬οΈβ¬οΈπ«π
βοΈπ
"""

message_switch_on = "π₯ Switch is ON"
message_switch_off = "π« Switch is OFF"
message_thermostat_on = "π΄ Thermostat is ON"
message_thermostat_off = "π’ Thermostat is OFF"
message_ready_to_shower = "π You can take shower now!"


def kwh(kwh_value):
    return f"π {kwh_value:.2f} KWh"


def get_time_message(text, time_seconds):
    min, sec = divmod(time_seconds, 60)
    if min > 59:
        hour, min = divmod(min, 60)
        t = f"{hour:02d}:{min:02d}:{sec:02d}"
    else:
        t = f"{min:02d}:{sec:02d}"
    return f"βοΈ {text}: {t}"


def multiline(msgs):
    return "\n".join(msgs)
