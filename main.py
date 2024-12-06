# main.py

from machine import Pin, SPI, UART
import utime
import st7789
from mh_z19 import MHZ19  # Ensure correct import based on your library
from font8x8 import font8x8_basic  # Replace with actual font object

# Configuration Constants
LCD_WIDTH = 135      # Adjust based on your display's resolution
LCD_HEIGHT = 240
LCD_ROTATION = 1     # 0: Portrait, 1: Landscape, 2: Inverted Portrait, 3: Inverted Landscape
CO2_THRESHOLD = 900  # CO₂ threshold in ppm for alert

# Initialize SPI for LCD
spi = SPI(1, baudrate=20000000, polarity=0, phase=0, sck=Pin(10), mosi=Pin(11))
dc = Pin(8, Pin.OUT)
cs = Pin(9, Pin.OUT)
rst = Pin(15, Pin.OUT)
bl = Pin(12, Pin.OUT)  # Backlight control pin

# Initialize LCD
lcd = st7789.ST7789(
    spi=spi,
    width=LCD_WIDTH,
    height=LCD_HEIGHT,
    reset=rst,
    dc=dc,
    cs=cs,
    backlight=bl,
    rotation=LCD_ROTATION,
    color_order=st7789.BGR
)
# No need to call lcd.init() as it's handled in the driver

# Initialize MH-Z19C sensor via UART1
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
sensor = MHZ19(uart_id=1, uart=uart)  # Adjust based on your library

# Initialize LED pin for alert (optional)
alert_led = Pin(16, Pin.OUT)

# Function to display CO2 and temperature on LCD
def display_co2(co2, temp):
    lcd.fill(st7789.BLACK)  # Clear the screen
    if co2 is not None and temp is not None:
        lcd.text(font8x8_basic, f"CO2: {co2} ppm", 10, 10, st7789.WHITE)
        lcd.text(font8x8_basic, f"Temp: {temp} C", 10, 30, st7789.WHITE)
        if co2 > CO2_THRESHOLD:
            alert_led.on()  # Turn on LED
            lcd.text(font8x8_basic, "ALERT!", 50, 120, st7789.RED)
        else:
            alert_led.off()  # Turn off LED
    else:
        lcd.text(font8x8_basic, "No Data", 10, 10, st7789.WHITE)

# Main Loop
while True:
    try:
        data = sensor.read()  # Updated method name
        co2 = data.get('co2')
        temp = data.get('temperature')
        print(f'CO2: {co2} ppm')
        print(f'Temperature: {temp} C')
        display_co2(co2, temp)
    except Exception as e:
        print(f"Error reading sensor: {e}")
        lcd.fill(st7789.BLACK)
        lcd.text(font8x8_basic, "Sensor Error", 10, 10, st7789.RED)
        alert_led.on()
    utime.sleep(2)  # Update every 2 seconds
