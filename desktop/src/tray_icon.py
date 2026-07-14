import logging

import pystray
from PIL import Image


from .state import State
from .serial import get_port_list


def init_tray_icon(state: State):
    state.tray_icon = pystray.Icon(
        "SpotifyAlbumArt",
        Image.open(state.icon_path),
        "Spotify Album Art",
        pystray.Menu(
            pystray.MenuItem("Button", _handle_test_button),
            pystray.MenuItem("Show Image", lambda: _handle_show_image(state)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Select USB Port", pystray.Menu(lambda: _rebuild_port_menu(state))),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", lambda: _handle_quit(state)),
        ),
    )


def _rebuild_port_menu(state: State):
    ports = get_port_list()
    menu_items = []
    if len(ports) == 0:
        state.selected_port = ""
        menu_items.append(pystray.MenuItem("No ports available", lambda: None, enabled=False))
    else:
        if len(ports) == 1:
            state.selected_port = ports[0].name
        for port in ports:
            menu_items.append(
                pystray.MenuItem(
                    f"{port.device} - {port.description}",
                    _mk_handle_select_port(state, port.device),
                    checked=_mk_is_port_checked(state, port.device),
                    radio=True,
                )
            )
    return [*menu_items, pystray.Menu.SEPARATOR, pystray.MenuItem("Refresh", _handle_refresh_port_menu)]


def _mk_handle_select_port(state: State, port: str):
    return lambda icon, item: _handle_select_port(icon, item, state, port)


def _handle_select_port(icon, item: pystray.MenuItem, state: State, port: str):
    logging.info(f"Selected port: {port}")
    state.selected_port = port
    icon.update_menu()


def _mk_is_port_checked(state: State, port: str):
    return lambda item: state.selected_port == port


def _handle_refresh_port_menu(icon):
    logging.info("Refreshing port list")
    icon.update_menu()


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
