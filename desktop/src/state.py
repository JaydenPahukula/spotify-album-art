from dataclasses import dataclass, field
import threading
from serial.tools.list_ports_common import ListPortInfo

from PIL import ImageFile
import pystray


@dataclass
class State:
    """
    Universal app state
    """

    ports: list[ListPortInfo] = field(default_factory=list)
    selected_port: ListPortInfo | None = None

    background_stop_event: threading.Event = None
    background_thread: threading.Thread = None

    tray_icon: type[pystray.Icon] = None

    image: ImageFile.ImageFile | None = None
