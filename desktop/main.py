import argparse
import logging
import os
import sys
from src.serial import select_last_used_port, update_port_list
from src.background_thread import init_background_thread
from src.tray_icon import init_tray_icon
from src.state import State

ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
LOG_FILE_PATH: str = os.path.join(ROOT_DIR, "desktop", "main.log")

_parser = argparse.ArgumentParser()
_parser.add_argument("--debug", action="store_true", help="run in debug mode")

if __name__ == "__main__":
    args = _parser.parse_args()

    state = State()

    logging.basicConfig(
        level="INFO",
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            *([logging.StreamHandler(sys.stdout)] if args.debug else []),
        ],
    )

    init_background_thread(state)
    init_tray_icon(state)
    select_last_used_port(state)
    update_port_list(state)

    # start the app!
    logging.info("================ Starting ================")
    state.background_thread.start()
    state.tray_icon.run()
