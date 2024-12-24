import serial
import time
import csv
from datetime import datetime
import serial
print(serial.__file__)

# Adjust to the correct serial port. Check with `ls /dev/tty.*` in Terminal.
SERIAL_PORT = '/dev/tty.usbmodem1101'  
BAUD_RATE = 9600

# CSV file to store data
CSV_FILE = 'co2_readings.csv'

# Initialize CSV if doesn't exist
with open(CSV_FILE, 'a', newline='') as f:
    writer = csv.writer(f)
    # If file is empty, write a header
    f.seek(0,2)
    if f.tell() == 0:
        writer.writerow(['timestamp', 'co2_ppm', 'temperature_c'])

# Open the serial port
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

try:
    while True:
        line = ser.readline().decode('utf-8', errors='replace').strip()
        # The Pico prints lines like: CO2 (ppm):400
        # Next line: Temperature (C):21
        # We need to parse them in pairs.
        if line.startswith('CO2 (ppm):'):
            co2_val = line.split(':')[1].strip()
            # Next line should be temperature
            temp_line = ser.readline().decode('utf-8', errors='replace').strip()
            temp_val = temp_line.split(':')[1].strip()
            # Append to CSV with a timestamp
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now().isoformat(), co2_val, temp_val])
except KeyboardInterrupt:
    ser.close()
