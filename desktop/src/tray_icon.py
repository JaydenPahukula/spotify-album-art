import logging
import os

import pystray
from PIL import Image
from serial.tools.list_ports_common import ListPortInfo
from src.serial import Msg, get_port_list, serial_send, update_selected_port
from src.state import exitApp, state

ICON_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "disk.png")


def init_tray_icon():
    state.tray_icon = pystray.Icon(
        "SpotifyAlbumArt",
        Image.open(ICON_PATH),
        "Spotify Album Art",
        pystray.Menu(
            pystray.MenuItem("Button", _handle_test_button),
            pystray.MenuItem("Show Image", _handle_show_image),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Select USB Port",
                pystray.Menu(_rebuild_port_menu),
                enabled=lambda _: not state.serial_establishing_connection,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", exitApp),
        ),
    )
    state.tray_icon.run_detached()


def _rebuild_port_menu():
    ports = get_port_list()
    menu_items = []
    if len(ports) == 0:
        menu_items.append(pystray.MenuItem("No ports available", lambda: None, enabled=False))
    else:
        for port in ports:
            menu_items.append(
                pystray.MenuItem(
                    f"{port.device} - {port.description}",
                    _mk_handle_select_port(port),
                    checked=_mk_is_port_checked(port),
                    radio=True,
                )
            )
    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(pystray.MenuItem("Refresh List", state.tray_icon.update_menu))
    if state.serial_connection.is_open:
        menu_items.append(pystray.MenuItem("Disconnect", _handle_disconnect))
    return menu_items


def _mk_handle_select_port(port: ListPortInfo):
    return lambda icon, item: _handle_select_port(icon, port)


def _handle_select_port(icon, port: ListPortInfo):
    logging.info("User selected port: " + port.device)
    update_selected_port(port.device)
    icon.update_menu()


def _mk_is_port_checked(port: ListPortInfo):
    return lambda item: state.serial_connection.port == port.device and state.serial_connection.is_open


def _handle_disconnect():
    logging.info("User selected disconnect")
    update_selected_port(None)
    state.tray_icon.update_menu()


def _handle_test_button():
    logging.info("TEST")
    serial_send(Msg.Test)


def _handle_show_image():
    if state.image is None:
        state.tray_icon.notify("Could not find a media thumbnail", " ")
    else:
        preview_image = state.image.resize(
            (state.image.width * 16, state.image.height * 16),
            Image.Resampling.NEAREST,
        )
        preview_image.show()
