# mh_z19.py

from machine import UART
import utime

class MHZ19:
    def __init__(self, uart_id=1, baudrate=9600, tx=4, rx=5):
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx, rx=rx)

    def read_co2(self):
        # Command to request CO2 reading
        cmd = bytearray([0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
        self.uart.write(cmd)
        utime.sleep(0.1)  # Wait for sensor to respond

        if self.uart.any() >= 9:
            resp = self.uart.read(9)
            if resp[0] == 0xFF and resp[1] == 0x86:
                co2 = resp[2] * 256 + resp[3]
                temp = resp[4] - 40  # Correct temperature calculation
                return {'co2': co2, 'temperature': temp}
        return {'co2': None, 'temperature': None}

