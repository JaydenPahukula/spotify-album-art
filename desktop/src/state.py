from dataclasses import dataclass, field
import threading
import serial
from serial.tools.list_ports_common import ListPortInfo

from PIL import ImageFile
import pystray


@dataclass
class State:
    """
    Universal app state
    """

    serial_establishing_connection: bool = False
    serial_connection = serial.Serial()

    background_stop_event: threading.Event = None
    background_thread: threading.Thread = None

    tray_icon: type[pystray.Icon] = None

    image: ImageFile.ImageFile | None = None
