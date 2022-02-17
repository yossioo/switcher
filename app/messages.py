ON_ICON = "🟥"
OFF_ICON = "⬛️"
READY_ICON = "🟠"
THERMOSTAT_ON = "🔴"
THERMOSTAT_OFF = "⚫️"

SHOWER1 = "🛁"
SHOWER2 = "🚿"
ALL_SYMBOLS = """
✅🚿🛁♨️☑️
🔘🔴🟠🟡🟢
🔵🟣⚫️⚪️🟤
🟥🟧🟨🟩🟦
🟪⬛️⬜️🟫🕑
⌛️🔋
"""

message_switch_on = "🟥 Switch is ON"
message_switch_off = "🟫 Switch is OFF"
message_thermostat_on = "🔴 Thermostat is ON"
message_thermostat_off = "🟢 Thermostat is OFF"
message_ready_to_shower = "🛁 You can take shower now!"


def kwh(kwh_value):
    return f"🔋 {kwh_value:.2f} KWh"


def get_time_message(text, time_seconds):
    min, sec = divmod(time_seconds, 60)
    if min > 59:
        hour, min = divmod(min, 60)
        t = f"{hour:02d}:{min:02d}:{sec:02d}"
    else:
        t = f"{min:02d}:{sec:02d}"
    return f"⌛️ {text}: {t}"


def multiline(msgs):
    return "\n".join(msgs)
