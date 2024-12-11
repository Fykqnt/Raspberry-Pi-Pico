from machine import Pin, UART, I2C
import ssd1306
import utime

mhz19c = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

while True:
    data = bytearray([0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    mhz19c.write(data)
    mhz19c.readinto(data,len(data))
    co2 = data[2] * 256 + data[3]
    temp = data[4] - 48
    print('CO2 (ppm):'+str(co2))
    print('Temperature (C):'+str(temp))

    display.fill(0)
    display.text('CO2:'+str(co2)+' ppm', 0, 0, 1)
    display.text('Temp:'+str(temp)+'degrees', 0, 10, 1)
    if co2 >= 1000:
            display.text('OPEN THE WINDOW', 0, 20, 1)
    display.show()

    utime.sleep(1)

