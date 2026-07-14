from dataclasses import dataclass
import os
import threading

from PIL import ImageFile
import pystray

_ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_LOG_FILE_PATH: str = os.path.join(_ROOT_DIR, "desktop", "main.log")
_ICON_PATH: str = os.path.join(_ROOT_DIR, "desktop", "assets", "disk.png")


@dataclass
class State:
    log_file_path: str = _LOG_FILE_PATH
    icon_path: str = _ICON_PATH

    selected_port: str = ""

    background_stop_event: threading.Event = None
    background_thread: threading.Thread = None

    tray_icon: type[pystray.Icon] = None

    image: ImageFile.ImageFile | None = None
