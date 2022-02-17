import time
import socket
import threading
import logging
import switcher_parser


class SwitcherClient:
    UDP_IP = "0.0.0.0"
    UDP_PORT = 20002

    def __init__(self):
        self.should_shutdown = False

        self._logger = logging.getLogger("SwitcherClient")
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(1.0)
        self._last_message_time = time.time() + 36000
        self._data = switcher_parser.SwitcherData()
        self._data_cbs = []

        self._t = threading.Thread(target=self.run)
        self._t.start()

    def add_data_listener(self, cb):
        self._data_cbs.append(cb)

    def run(self):
        try:
            self._sock.bind((self.UDP_IP, self.UDP_PORT))
        except Exception as e:
            print(e)

        while not self.should_shutdown:
            now = time.time()
            try:
                raw_data, addr = self._sock.recvfrom(1024)
                self._last_message_time = now
            except socket.timeout as e:
                sec_since_update = now - self._last_message_time
                if sec_since_update > 30 and sec_since_update % 30 < 1:
                    self._logger.warn(
                        f"No messages from Switcher for {sec_since_update:.1f} seconds"
                    )
                continue
            self._data = switcher_parser.parse_data(raw_data)
            self._logger.info(self._data)
            for cb in self._data_cbs:
                cb(self._data)
        self._logger.warn("Shutting down")
