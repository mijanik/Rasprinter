import time
import serial
import re
import board
import busio
import adafruit_ssd1306
import adafruit_bmp280
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

ser = None
i2c = None
oled = None
MyOlED = None

def init_IO():
    print("Initializing GPIO")
    global GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(12, GPIO.OUT) # Relay
    GPIO.setup(13, GPIO.OUT) # LED
    GPIO.setup(19, GPIO.OUT) # LED
    GPIO.setup(26, GPIO.OUT) # LED
    GPIO.output(12, 0)
    GPIO.output(13, 0)
    GPIO.output(19, 0)
    GPIO.output(26, 0)

    GPIO.output(12, 1) # Turn on Printer Relay
    time.sleep(15)     # Wait for printer to start
    
    print("Initializing serial connection to printer at /dev/ttyACM0, baudrate 115200")
    global ser 
    try:    
        ser = serial.Serial(port='/dev/ttyACM0', baudrate = 115200, timeout=1)
        ser.reset_input_buffer()
    except Exception as e:
        print(f"An error occurred while initializing serial connection to printer: {e}")
    
    print("Initializing I2C Bus")
    global i2c 
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
    except Exception as e:
        print(f"An error occurred while initializing I2C: {e}")
    
    print("Initializing OLED")
    global oled
    global MyOLED
    try:
        oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
        MyOLED = OLEDStatus()
    except Exception as e:
        print(f"An error occurred while initializing OLED screen: {e}")

    print("Rasprinter is ready")

class OLEDStatus:
    def __init__(self):
        self.CurrentState = "OFF"
        self.Text = "OFF"

def set_relay(RelayStatus: str):
    # ON or OFF
    
    global GPIO
    
    if RelayStatus == "ON":
        GPIO.output(12, 1)
    elif RelayStatus == "OFF":
        GPIO.output(12, 0)
    else:
        print("set_relay - Invalid Parameter!")

def set_LED(LED_Color: str, LED_Status):
    # Sets Color 
    # RED or GREEN or BLUE
    # ON or OFF
    
    global GPIO
    if LED_Color == 'RED':
        if LED_Status == 'ON' or LED_Status == 1:
            GPIO.output(13, 1)
        elif LED_Status == 'OFF' or LED_Status == 0:
            GPIO.output(13, 0)
    elif LED_Color == 'GREEN':
        if LED_Status == 'ON' or LED_Status == 1:
            GPIO.output(19, 1)
        elif LED_Status == 'OFF' or LED_Status == 0:
            GPIO.output(19, 0)
    elif LED_Color == 'BLUE':
        if LED_Status == 'ON' or LED_Status == 1:
            GPIO.output(26, 1)
        elif LED_Status == 'OFF' or LED_Status == 0:
            GPIO.output(26, 0)


def status_OLED(state):
    # Shows Monitor status on OLED display
    
    global MyOLED
    
    if state == "ON" and MyOLED.CurrentState != "ON":
        MyOLED.Text = "Monitor is ON"
        MyOLED.CurrentState = "ON"
        print_OLED(MyOLED.Text)
    elif state == "OFF" and MyOLED.CurrentState != "OFF":
        MyOLED.Text = "Monitor is OFF"
        MyOLED.CurrentState = "OFF"
        print_OLED(MyOLED.Text)
        
def print_OLED(text):
    # Shows standard text on OLED display
    
    global oled
    
    try:
        oled.fill(0)
        oled.show()

        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        
        (font_width, font_height) = font.getsize(text)
        draw.text(
            (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
            text,
            font=font,
            fill=255,
        )
        
        oled.image(image)
        oled.show()
    except Exception as e:
        print(f"An error occurred during communication with OLED Screen: {e}")


def emergency_stop_M112():
    # uses M112 marlin command
    # Used for emergency stopping, M112 shuts down the machine, 
    # turns off all the steppers and heaters. 
    # A reset is required to return to operational mode.
    
    global ser
    
    try:
        ser.write(b"M112\n")
        time.sleep(0.1)
        print("Used command <M112>")
    except Exception as e:
        print(f"An error occurred while sending M112 Emergency Stop: {e}")

def play_tone_M300():
    # uses M300 marlin command
    # Play tone - require speaker to playtones - not just beeps
    # need beep duration and frequency parameters
    
    global ser
    
    try:
        ser.write(b"M300\n")
        time.sleep(1)
        while ser.in_waiting < 2:
            time.sleep(0.01)
        line = ser.readline().decode('utf-8').rstrip()
        if line == "ok":
            print("Used command <M300>")
    except Exception as e:
        print(f"An error occurred while sending M300 Play Tone: {e}")

def get_temp_M105():
    # uses M105 marlin command (need global serial variable "ser")
    # returns tuple of:
    # current printhead temperature
    # destination printhead temperature
    # current printbed temperature
    # destination printbed temperature

    global ser
    head_curr_temp = 0
    head_dest_temp = 0
    bed_curr_temp = 0
    bed_dest_temp = 0

    try:
        ser.write(b"M105\n")
        print("Used command <M105>")
        time.sleep(0.1)
    except Exception as e:
        print(f"An error occurred while sending M105 command: {e}")
    
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            
            result = re.search('ok T:(.*?) /', line)
            head_curr_temp = result.group(1)
            
            result = re.search(' /(.*?) B:', line)
            head_dest_temp = result.group(1)

            result = re.search(' B:(.*?) /', line)
            bed_curr_temp = result.group(1)

            result = re.search(' B:(.*?) @:', line)
            bed_dest_temp = result.group(1).split("/", 1)[1]
    except Exception as e:
        print(f"An error occurred while receiving M105 printer \
              temperature information: {e}")

    return float(head_curr_temp), float(head_dest_temp), float(bed_curr_temp), float(bed_dest_temp)


def get_temp_hum_HTU21D():
    # Returns tuple of float value of Temperature and Humidity
    # HTU21D address = 0x40
    # Read temp - No-hold master mode (no clock stretching) = 0xF3
    
    global i2c
    temp_raw = bytearray(2)
    hum_raw = bytearray(2)
    temperature = 0
    humidity = 0
    
    try:
        # Read and calculate temperature data
        i2c.writeto(0x40, bytes([0xF3]), stop=False) 
        time.sleep(0.1)
        i2c.readfrom_into(0x40, temp_raw)
        temp_raw_int = temp_raw[0] * 256 + temp_raw[1]
        temperature = ((175.72 * temp_raw_int)/65536)-48.85
        
        # Read and calculate humidity data
        i2c.writeto(0x40, bytes([0xF5]), stop=False) 
        time.sleep(0.1)
        i2c.readfrom_into(0x40, hum_raw)
        hum_raw_int = hum_raw[0] * 256 + hum_raw[1]
        humidity = ((125 * hum_raw_int)/65536)-6
        
    except Exception as e:
        print(f"An error occurred during communication with HTU21D sensor: {e}")
    
    return round(temperature, 2), round(humidity, 2)

def get_temp_hum_SHT31():
    # Returns tuple of float value of Temperature and Humidity
    # SHT31 address = 0x44
    # CRC checksum not used
    # 2 bytes 0x24 and 0x16 means quick measurment with no clock stretching
    
    global i2c
    temp_hum_raw = bytearray(6)
    temperature = 0
    humidity = 0
    
    try:
        # Read raw temperature and humidity data
        i2c.writeto(0x44, bytearray([0x24, 0x16]), stop=False) 
        time.sleep(0.1)
        i2c.readfrom_into(0x44, temp_hum_raw)
        
        # Calculate/decode received data
        temperature = temp_hum_raw[0] * 256 + temp_hum_raw[1]
        temperature = (175 * temperature / 65535) - 45
        humidity = 100 * (temp_hum_raw[3] * 256 + temp_hum_raw[4]) / 65535
        
    except Exception as e:
        print(f"An error occurred during communication with SHT31 sensor: {e}")
    
    return round(temperature, 2), round(humidity, 2)

def get_temp_press_BMP280():
    # Returns tuple of float value of Temperature and Pressure
    
    global i2c
    temperature = 0
    pressure = 0
    
    try:
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address = 0x76)
        temperature = sensor.temperature
        pressure = sensor.pressure
    except Exception as e:
        print(f"An error occurred during communication with BMP280 sensor: {e}")
        
    return round(temperature, 2), round(pressure, 2)