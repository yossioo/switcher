#!/usr/bin/env python3
import os
import coloredlogs
from pyro_client import PyroClient
from switcher_client import SwitcherClient


if __name__ == "__main__":
    coloredlogs.install(
        level="INFO", fmt="%(asctime)s [%(name)s] %(levelname)s %(message)s"
    )
    sc = SwitcherClient()
    pc = PyroClient()
    sc.add_data_listener(pc.update_data)
    pc.send_info_msg()
    pc.spin()
    sc.should_shutdown = True
    print("main done")
