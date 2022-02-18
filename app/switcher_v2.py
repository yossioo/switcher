#!/usr/bin/env python3
import os
import coloredlogs
from pyro_client import PyroClient
from switcher_client import SwitcherClient


def install_coloredlogs(loggers):
    level = os.getenv("LOGLEVEL")
    if level is None:
        level = "INFO"
    for l in loggers:
        coloredlogs.install(
            level=level,
            fmt="%(asctime)s [%(name)s] %(levelname)s %(message)s",
            logger=l,
        )


if __name__ == "__main__":
    sc = SwitcherClient()
    pc = PyroClient()
    install_coloredlogs([sc._logger, pc._logger])
    sc.add_data_listener(pc.update_data)
    pc.send_info_msg("🔌 I'm online! 📡")
    pc.spin()
    sc.should_shutdown = True
    print("main done")
