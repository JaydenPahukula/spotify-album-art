import logging
import os

import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo

from src.state import State


LAST_PORT_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".port")


def update_port_list(state: State):
    state.ports = serial.tools.list_ports.comports()


def select_port(state: State, port: str):
    if port == state.selected_port:
        return
    logging.info("Selected port: " + port)
    state.selected_port = port
    _save_port_file(port)


def select_last_used_port(state: State):
    try:
        with open(LAST_PORT_PATH, "r") as file:
            port = file.readline().strip()

        if len(port) == 0:
            return
        logging.info("Using previously selected port: " + port)
        state.selected_port = port

    except FileNotFoundError:
        pass  # .port file does not exist


def _save_port_file(port: ListPortInfo):
    # make parent dirs if necessary
    os.makedirs(os.path.dirname(LAST_PORT_PATH), exist_ok=True)
    # write file
    with open(LAST_PORT_PATH, "w") as file:
        file.write(port)


def _update_serial_connection(state: State):
    pass
