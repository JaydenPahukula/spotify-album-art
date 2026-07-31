import threading
from dataclasses import dataclass
from tkinter import Tk

import pystray
import serial
from PIL import ImageFile


@dataclass
class State:
    """
    Universal app state
    """

    debug: bool = False

    serial_establishing_connection: bool = False
    serial_connection = serial.Serial()

    background_stop_event: threading.Event = None
    background_thread: threading.Thread = None

    tray_icon: pystray.Icon = None

    image: ImageFile.ImageFile | None = None

    last_media_key: str | None = None

    gui_root: Tk = None
    gui_icon_photo: ImageFile.ImageFile | None = None
