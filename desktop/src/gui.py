import ctypes
import logging
import os
from tkinter import Label, Tk, Toplevel

from PIL import Image, ImageTk
from src.state import State

IMAGE_SCALE = 6  # how much to scale up the 64x64 pixel image for viewing
ICON_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "disk.png")

_preview_window: Toplevel | None = None
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("asdf")
except Exception:
    pass


def init_gui(state: State):
    state.gui_root = Tk()
    state.gui_root.withdraw()


def gui_show_preview(state: State):
    state.gui_root.after(0, _show_preview_window, state)


def _show_preview_window(state: State):
    global _preview_window
    # init preview gui if needed
    if _preview_window is None or not _preview_window.winfo_exists():
        _preview_window = Toplevel(state.gui_root)
        _preview_window.title = "Preview"

        # load the icon if needed
        if state.gui_icon_photo is None:
            try:
                state.gui_icon_photo = Image.open(ICON_PATH)
            except Exception as e:
                logging.error(f"Error loading gui icon: {e}")

        if state.gui_icon_photo is not None:
            icon_photo = ImageTk.PhotoImage(state.gui_icon_photo)
            _preview_window.iconphoto(False, icon_photo)
            _preview_window._icon = icon_photo
    # otherwise clear current image
    else:
        [w.destroy() for w in _preview_window.winfo_children()]
    preview_photo = ImageTk.PhotoImage(
        state.image.resize(
            (state.image.width * IMAGE_SCALE, state.image.height * IMAGE_SCALE), Image.Resampling.NEAREST
        )
    )
    label = Label(_preview_window, image=preview_photo)
    label.image = preview_photo
    label.pack()

    _preview_window.deiconify()
    _preview_window.lift()
