import logging
import threading
from dataclasses import dataclass

import pystray
import serial
from PIL import ImageFile


@dataclass
class State:
    debug: bool = False

    serial_establishing_connection: bool = False
    serial_connection = serial.Serial()

    background_stop_event: threading.Event = None
    background_thread: threading.Thread = None

    tray_icon: pystray.Icon = None

    image: ImageFile.ImageFile | None = None

    last_media_key: str | None = None

    gui_icon_photo: ImageFile.ImageFile | None = None

    exited: bool = False


state = State()
"""Universal app state"""


def exitApp(signum=None, frame=None):
    logging.info("Exiting")
    state.tray_icon.stop()
    state.exited = True
