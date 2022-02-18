import logging
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from switcher_parser import SwitcherData
import messages


def load_users():
    import yaml

    with open("users.yaml", "r") as stream:
        parsed_yaml = yaml.safe_load(stream)
        return parsed_yaml["ids"]


class PyroClient:
    def __init__(self):
        self._logger = logging.getLogger("PyroClient")
        self._users = load_users()
        self._app = Client("bot")
        self._latest_start_messages = dict()
        self._app.add_handler(
            MessageHandler(self.cb_start_cmd, filters=filters.command(["start"]))
        )

        def callback_query(client, query):
            self._logger.info(f"Got callback_query(..): {query.data}")
            if query.data == "refresh_time":
                self.send_info_msg()

        self._app.add_handler(CallbackQueryHandler(callback_query))
        self._data = SwitcherData()
        # Ready to work

        self._app.start()
        self._logger.info("PyroClient is ready now!")
        # self._app.send_message(
        #     self._users[0],
        #     "**PyroClient is ready now**",
        # )

    def update_data(self, data: SwitcherData):
        self._logger.debug(f"Got data: {data}")
        data_changed = False
        if data.is_on != self._data.is_on:
            self._logger.info("Data is_on changed, updating the message")
            data_changed = True
        if data.active() != self._data.active():
            self._logger.info("Data active() changed, updating the message")
            data_changed = True
        self._data = data
        if data_changed:
            self.send_info_msg()

    def spin(self):
        self._logger.info("PyroClient going idle...")
        idle()
        self._logger.warn("idle() done")

    def cb_start_cmd(self, client, message):
        self.send_info_msg()

    def get_markup(self, text_values):
        rows = []
        for row_txt in text_values:
            row = []
            for btn_txt in row_txt:
                if isinstance(btn_txt, str):
                    row.append(InlineKeyboardButton(btn_txt, callback_data="-"))
                elif isinstance(btn_txt, tuple):
                    row.append(
                        InlineKeyboardButton(btn_txt[0], callback_data=btn_txt[1])
                    )
                else:
                    self._logger.warn(
                        f"get_markup(..): Cannot add item {btn_txt} of type {type(btn_txt)}"
                    )
            rows.append(row)
        return InlineKeyboardMarkup(rows)

    def get_full_keyboard(self):
        state = [
            messages.message_switch_on
            if self._data.is_on
            else messages.message_switch_off,
            messages.message_thermostat_on
            if self._data.active()
            else messages.message_thermostat_off,
        ]

        consumption = [
            (messages.get_time_message("Active", 3878), "refresh_time"),
            messages.kwh(10.456),
        ]

        return self.get_markup(
            [
                state,
                consumption,
                [(f"ON for: {self._data.on_duration()}", "refresh_time")],
            ]
            if self._data.is_on
            else [
                state,
                consumption,
            ]
        )

    def send_info_msg(self):
        for u in self._users:
            k = int(u)
            if self._latest_start_messages.get(k):
                message = self._latest_start_messages.get(k)
                self._logger.debug(f"Deleting message {message.message_id} for user {k}")
                self._app.delete_messages(k, int(message.message_id))
            self._latest_start_messages[k] = self._app.send_message(
                u,
                "••••••••••••••••••••\n\n🔌 I'm online! 📡",
                reply_markup=self.get_full_keyboard(),
                # reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Hello")]]),
            )
