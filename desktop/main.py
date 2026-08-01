import argparse
import ctypes
import logging
import os
import signal
import sys
import time

from src.background_thread import initialize_background_thread
from src.serial import initialize_serial
from src.state import exitApp, state
from src.tray_icon import init_tray_icon

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Spotify Album Art")
except AttributeError:
    pass

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
LOG_FILE_PATH: str = os.path.join(ROOT_DIR, "desktop", "main.log")

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="run in debug mode")
    args = parser.parse_args()
    state.debug = args.debug

    logging.basicConfig(
        level="INFO",
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            *([logging.StreamHandler(sys.stdout)] if state.debug else []),
        ],
    )

    signal.signal(signal.SIGINT, exitApp)
    signal.signal(signal.SIGTERM, exitApp)

    initialize_background_thread()
    initialize_serial()
    init_tray_icon()

    logging.info("Started")

    # if debug mode, keep the main thread open to catch signals
    if state.debug:
        while not state.exited:
            time.sleep(0.2)
