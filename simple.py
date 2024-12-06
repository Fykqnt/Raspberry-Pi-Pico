from machine import Pin, UART
import utime

mhz19c = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

while True:
    data = bytearray([0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    mhz19c.write(data)
    mhz19c.readinto(data,len(data))
    co2 = data[2] * 256 + data[3]
    temp = data[4] - 48
    print('CO2 (ppm):'+str(co2))
    print('Temperature (C):'+str(temp))

    utime.sleep(1)
