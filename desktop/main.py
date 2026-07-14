import argparse
import logging
import sys
from src.background_thread import init_background_thread
from src.tray_icon import init_tray_icon
from src.state import State

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="run in debug mode")

if __name__ == "__main__":
    args = parser.parse_args()

    state = State()

    logging.basicConfig(
        level="INFO",
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(state.log_file_path),
            *([logging.StreamHandler(sys.stdout)] if args.debug else []),
        ],
    )

    init_background_thread(state)
    init_tray_icon(state)

    # start the app!
    logging.info("================ Starting ================")
    state.background_thread.start()
    state.tray_icon.run()
