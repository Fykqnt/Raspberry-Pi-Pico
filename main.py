from machine import Pin, UART, I2C
import ssd1306
import utime
import network
import urequests
import ujson

# -------------------- Configuration --------------------

# Wi-Fi credentials
WIFI_SSID = 'xxxxxxxxxx'
WIFI_PASSWORD = 'xxxxxxxxxx'

# Slack webhook URL
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/xxxxxxxxxx'

# CO2 threshold
CO2_THRESHOLD = 1000  # ppm

# --------------------------------------------------------
# Initialize UART for MH-Z19C
mhz19c = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Initialize I2C for SSD1306 display
i2c = I2C(0, sda=Pin(0), scl=Pin(1))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Flag to track previous CO2 state
previous_above_threshold = False

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            utime.sleep(1)
            print('.', end='')
    print('\nWi-Fi connected:', wlan.ifconfig())

def send_slack_notification(message_text):
    try:
        headers = {'Content-Type': 'application/json'}
        
        # Minimal payload
        message = {"text": message_text}
        
        # Serialize JSON
        json_data = ujson.dumps(message)
        
        # Print the payload for debugging
        print('Sending payload:', json_data)
        
        # Send the POST request with encoded data
        response = urequests.post(SLACK_WEBHOOK_URL, data=json_data.encode('utf-8'), headers=headers)
        
        # Print response status and body
        print('Slack response status:', response.status_code)
        try:
            response_text = response.text
            print('Slack response body:', response_text)
        except:
            print('No response body available.')
        
        if response.status_code == 200:
            print('Slack notification sent successfully.')
        else:
            print('Failed to send Slack notification. Status code:', response.status_code)
        
        response.close()
    except Exception as e:
        print('Error sending Slack notification:', e)

# Connect to Wi-Fi
connect_wifi(WIFI_SSID, WIFI_PASSWORD)

# Test the Slack webhook with a minimal message
print('\n--- Testing Slack Webhook ---')
send_slack_notification("Test message from Raspberry Pi Pico W")

# Main Loop (Will execute only after the test)
while True:
    # Request CO2 and temperature data from MH-Z19C
    request_data = bytearray([0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
    mhz19c.write(request_data)
    utime.sleep(0.1)  # Wait for sensor to process

    response = bytearray(9)
    mhz19c.readinto(response, len(response))

    # Calculate CO2 ppm and temperature
    co2 = response[2] * 256 + response[3]
    temp = response[4] - 48

    print('CO2 (ppm):', co2)
    print('Temperature (C):', temp)

    # Update display
    display.fill(0)
    display.text(f'CO2: {co2} ppm', 0, 0, 1)
    display.text(f'Temp: {temp} degrees', 0, 10, 1)

    if co2 >= CO2_THRESHOLD:
        display.text('OPEN THE WINDOW', 0, 20, 1)
        if not previous_above_threshold:
            send_slack_notification(f"High CO₂ Level Detected!\nCO₂: {co2} ppm\nTemperature: {temp}°C\nPlease ventilate the area.")
            previous_above_threshold = True
    else:
        previous_above_threshold = False  # Reset when below threshold

    display.show()

    utime.sleep(1)
