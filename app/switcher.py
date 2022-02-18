#!/usr/bin/python3
import os
import time
import logging
import coloredlogs
import socket
import traceback
import yaml

from pyrogram import Client, filters

import switcher_parser
from notifier import Notifier

# if os.getenv("COLORED") is not None:
# value = os.getenv("COLORED").lower()
# if value == "true":
os.environ["DEFAULT_LOG_FORMAT"] = "%(asctime)s [%(name)s] %(levelname)s %(message)s"
coloredlogs.install(level="INFO")

logging.getLogger("pyrogram.session.session").setLevel(logging.WARNING)
logger = logging.getLogger("PyroSwV2")
logger.setLevel(logging.DEBUG)

UDP_IP = "0.0.0.0"
UDP_PORT = 20002

ON_ICON = "🟥"
OFF_ICON = "⬛️"
READY_ICON = "🟠"
THERMOSTAT_ON = "🔴"
THERMOSTAT_OFF = "⚫️"
ALL_SYMBOLS = "✅🟥🟧🟨🟩🟦🟪⬛️⬜️🟫🔴🟠🟡🟢🔵🟣⚫️⚪️🟤"

users = []
with open("users.yaml", "r") as stream:
    try:
        parsed_yaml = yaml.safe_load(stream)
        users = parsed_yaml["ids"]
    except yaml.YAMLError as exc:
        logger.error(exc)


app = Client("bot")
logger.info("Created the client")


def send_msg(text, silent=True):
    logger.debug(f"Sending '{text}' to users:")
    for user in users:
        ok = False
        try:
            app.send_message(user, text, disable_notification=silent)
            ok = True
        except Exception:
            pass
        logger.debug(f"\t{user}: {'OK' if ok else 'FAIL'}")
        if not ok:
            logger.error(f"Failed to send message to user: {user}")


notifier = Notifier(send_msg)


@app.on_message(filters.private)
async def hello(client, message):
    sender = message.from_user.first_name
    text = message.text
    if text == "/status":
        await message.reply(f"**Latest Data:**\n{notifier._prev_data}")
        return
    logger.info(f"Got message from {sender}: {text}")
    await message.reply(f"Hello! ✅\n{text}")


to_sec = 1.0
with app:
    # send_msg("I'm up! " + ALL_SYMBOLS)
    logger.info("Up and running!")
    send_msg("I'm up! ")
    try:
        logger.info("Opening socket for switcher")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(to_sec)
        sock.bind((UDP_IP, UDP_PORT))
        logger.info("Listening for messages")
        while True:
            try:
                raw_data, addr = sock.recvfrom(1024)
            except socket.timeout as e:
                # logger.info(f"-------No messages from the switcher for {to_sec} seconds...")
                continue
            try:
                data = switcher_parser.parse_data(raw_data)
                notifier.update(data)
                logger.info(f" <<< {data}")
            except Exception as e:
                logger.info(f"====== Exception ======\n{e}")
    except KeyboardInterrupt:
        logger.info("Ctrl-C pressed - stopping")
    except Exception as e:
        logger.info(f"[!] Something went wrong... {type(e)}")
        logger.info("[!] " + str(e))
        logger.info("---------------------")
        traceback.print_exc()
        logger.info("---------------------")
