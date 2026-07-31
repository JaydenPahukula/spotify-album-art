import argparse
import ctypes
import logging
import os
import sys

from src.background_thread import initialize_background_thread
from src.gui import init_gui
from src.serial import initialize_serial
from src.state import State
from src.tray_icon import init_tray_icon

try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("asdf")
except AttributeError:
    pass

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
LOG_FILE_PATH: str = os.path.join(ROOT_DIR, "desktop", "main.log")

_parser = argparse.ArgumentParser()
_parser.add_argument("--debug", action="store_true", help="run in debug mode")

if __name__ == "__main__":
    args = _parser.parse_args()

    state = State()
    state.debug = args.debug

    logging.basicConfig(
        level="INFO",
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            *([logging.StreamHandler(sys.stdout)] if state.debug else []),
        ],
    )
    logging.info("Started")

    init_gui(state)
    initialize_background_thread(state)
    init_tray_icon(state)
    initialize_serial(state)

    logging.info("Done initializing")
    state.gui_root.mainloop()
