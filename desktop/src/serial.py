import enum
import logging
import os
import threading
import time

import serial.tools.list_ports
from serial.serialutil import SerialException
from serial.tools.list_ports_common import ListPortInfo
from src.state import state

BAUD_RATE = 115200
LAST_PORT_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".port")

# flag to tell the listener thread when the serial connection is open
_connection_open_flag = threading.Event()


class Msg(enum.Enum):
    Test = 0
    Image = 1
    NoImage = 2


def initialize_serial():
    state.serial_connection.baudrate = BAUD_RATE
    # start the background listener thread
    _connection_open_flag.clear()
    threading.Thread(target=_listener_thread, daemon=True).start()
    # check for a last used port
    try:
        with open(LAST_PORT_PATH, "r") as file:
            port = file.readline().strip()
        if len(port) > 0:
            logging.info("Selected previously used port: " + port)
            _switch_port(port)
    except FileNotFoundError:
        pass  # .port file does not exist


def get_port_list() -> list[ListPortInfo]:
    return sorted(serial.tools.list_ports.comports(), key=lambda port: port.device)


def update_selected_port(port: str | None) -> bool:
    if port == state.serial_connection.port and state.serial_connection.is_open:
        return
    _switch_port(port, True)


def _switch_port(new_port: str | None, notify_on_fail: bool = False):
    # switch ports in the background
    threading.Thread(target=_switch_port_thread, args=[new_port, notify_on_fail], daemon=True).start()


def _switch_port_thread(new_port: str | None, notify_on_fail: bool):
    if state.serial_establishing_connection:
        return
    state.serial_establishing_connection = True
    state.tray_icon.update_menu()

    conn = state.serial_connection

    # close current connection if needed
    if conn.is_open:
        _connection_open_flag.clear()
        conn.close()
        logging.info("Closed serial connection on " + conn.port)

    conn.port = new_port

    # open new connection
    if new_port is not None:
        try:
            conn.open()
            time.sleep(2)
            _connection_open_flag.set()
            logging.info("Opened serial connection on " + conn.port)
        except SerialException:
            _connection_open_flag.clear()
            logging.info("Failed to open serial connection on " + conn.port)
            if notify_on_fail:
                state.tray_icon.notify("Failed to connect to device on " + conn.port)
            conn.port = None

    _save_last_port(conn.port)
    state.serial_establishing_connection = False
    state.tray_icon.update_menu()


def _save_last_port(port: str | None):
    # make parent dirs if necessary
    os.makedirs(os.path.dirname(LAST_PORT_PATH), exist_ok=True)
    # write file
    data = "" if port is None else port
    with open(LAST_PORT_PATH, "w") as file:
        file.write(data)


def _listener_thread():
    while True:
        # wait until serial connection is open
        _connection_open_flag.wait()
        conn = state.serial_connection
        if not conn.is_open:
            # connection isn't open, try again in a second
            time.sleep(1)
            continue
        try:
            data = conn.readline().decode()
            if len(data) == 0:
                continue
            _process_message(data)
        except (serial.SerialException, OSError):
            _connection_open_flag.clear()
            conn.close()
            state.tray_icon.update_menu()
            logging.info("Lost serial connection on " + conn.port)


def _process_message(msg: str):
    logging.info("Yippee! Recieved message: " + msg)


def serial_send(msg: Msg, data: bytes | None = None):
    # TODO
    if msg == Msg.Test:
        pass
    elif msg == Msg.Image:
        pass
    elif msg == Msg.NoImage:
        pass
    else:
        pass


def _send(data: str):
    conn = state.serial_connection
    if conn.is_open:
        conn.write(b"<HELLO>")
