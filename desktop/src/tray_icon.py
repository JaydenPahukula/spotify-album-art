import logging
import os

import pystray
from PIL import Image
from serial.tools.list_ports_common import ListPortInfo

from src.serial import get_port_list, update_selected_port
from src.state import State


ICON_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "disk.png")


def initialize_tray_icon(state: State):
    state.tray_icon = pystray.Icon(
        "SpotifyAlbumArt",
        Image.open(ICON_PATH),
        "Spotify Album Art",
        pystray.Menu(
            pystray.MenuItem("Button", _handle_test_button),
            pystray.MenuItem("Show Image", lambda: _handle_show_image(state)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Select USB Port",
                pystray.Menu(lambda: _rebuild_port_menu(state)),
                enabled=lambda _: not state.serial_establishing_connection,
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", lambda: _handle_quit(state)),
        ),
    )


def _rebuild_port_menu(state: State):
    ports = get_port_list()
    menu_items = []
    if len(ports) == 0:
        menu_items.append(pystray.MenuItem("No ports available", lambda: None, enabled=False))
    else:
        for port in ports:
            menu_items.append(
                pystray.MenuItem(
                    f"{port.device} - {port.description}",
                    _mk_handle_select_port(state, port),
                    checked=_mk_is_port_checked(state, port),
                    radio=True,
                )
            )
    menu_items.append(pystray.Menu.SEPARATOR)
    menu_items.append(pystray.MenuItem("Refresh", lambda: _handle_refresh_port_menu(state)))
    if state.serial_connection.is_open:
        menu_items.append(pystray.MenuItem("Disconnect", lambda: _handle_disconnect(state)))
    return menu_items


def _mk_handle_select_port(state: State, port: ListPortInfo):
    return lambda icon, item: _handle_select_port(icon, state, port)


def _handle_select_port(icon, state: State, port: ListPortInfo):
    logging.info("User selected port: " + port.device)
    update_selected_port(state, port.device)
    icon.update_menu()


def _mk_is_port_checked(state: State, port: ListPortInfo):
    return lambda item: state.serial_connection.port == port.device and state.serial_connection.is_open


def _handle_refresh_port_menu(state: State):
    state.tray_icon.update_menu()


def _handle_disconnect(state: State):
    logging.info("User selected disconnect")
    update_selected_port(state, None)
    state.tray_icon.update_menu()


def _handle_test_button():
    logging.info("TEST")


def _handle_show_image(state: State):
    if state.image is None:
        pystray.Icon.notify(state.tray_icon, "No image found :(")
    else:
        state.image.show()


def _handle_quit(state: State):
    logging.info("Exiting")

    # stop the background thread
    state.background_stop_event.set()
    state.background_thread.join()

    state.tray_icon.stop()
