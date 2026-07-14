import serial.tools.list_ports
import serial.tools.list_ports_common


def get_port_list() -> list[serial.tools.list_ports_common.ListPortInfo]:
    return serial.tools.list_ports.comports()


# TODO move port_list into State
