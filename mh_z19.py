# mh_z19.py

import struct
import utime
from machine import UART

class MHZ19:
    """
    MH-Z19C CO2 Sensor Driver

    Args:
        uart_id (int): UART identifier (e.g., 1 for UART1)
        uart (UART): UART object
    """

    def __init__(self, uart_id=1, uart=None):
        if uart is None:
            self.uart = UART(uart_id, baudrate=9600, tx=4, rx=5)
        else:
            self.uart = uart
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self.initialize()

    def initialize(self):
        """
        Initialize the sensor (optional).
        """
        # Example: Turn off auto-calibration
        self.send_command([0x94, 0x04, 0x00])

    def send_command(self, cmd):
        """
        Send a command to the sensor.

        Args:
            cmd (list): List of command bytes.
        """
        checksum = self.calculate_checksum(cmd)
        command = bytes(cmd + [checksum])
        self.uart.write(command)
        utime.sleep_ms(100)

    def calculate_checksum(self, cmd):
        """
        Calculate checksum for a command.

        Args:
            cmd (list): List of command bytes.

        Returns:
            int: Checksum byte.
        """
        return 0xFF - (sum(cmd) & 0xFF) + 1

    def read_response(self):
        """
        Read response from the sensor.

        Returns:
            bytes: Response bytes.
        """
        response = self.uart.read(9)
        return response

    def read_co2(self):
        """
        Read CO2 concentration and temperature from the sensor.

        Returns:
            dict: Dictionary containing 'co2' and 'temperature'.
        """
        # Send command to read CO2 concentration
        self.send_command([0x86])
        response = self.read_response()
        if response is None or len(response) < 9:
            return {'co2': None, 'temperature': None}

        if self.verify_checksum(response):
            co2 = response[2] * 256 + response[3]
            temperature = response[4] - 40  # Temperature offset
            return {'co2': co2, 'temperature': temperature}
        else:
            return {'co2': None, 'temperature': None}

    def verify_checksum(self, response):
        """
        Verify the checksum of the response.

        Args:
            response (bytes): Response bytes.

        Returns:
            bool: True if checksum is valid, False otherwise.
        """
        checksum = response[-1]
        calculated = 0xFF - (sum(response[:-1]) & 0xFF) + 1
        return checksum == calculated
