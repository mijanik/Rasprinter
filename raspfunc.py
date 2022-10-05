import time
import serial
import re
import board
import busio
import adafruit_ssd1306
import adafruit_bmp280
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO


#from sensor_database import MyOLED
class OLEDStatus:
    def __init__(self):
        self.CurrentState = "OFF"
        self.Text = "OFF"


print("Initializing LEDs")
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.output(13, 0)
GPIO.output(19, 0)
GPIO.output(26, 0)

print("Initializing serial connection to printer at /dev/ttyACM0, 115200")
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 115200,
    timeout=1
)
ser.reset_input_buffer()

print("Initializing I2C Bus")
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

MyOLED = OLEDStatus()

print("OK")


#RED or GREEN or BLUE
#ON or OFF
def set_LED(LED_Color: str, LED_Status):

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
    if state == "ON" and MyOLED.CurrentState != "ON":
        MyOLED.Text = "Monitor is ON"
        MyOLED.CurrentState = "ON"
        print_OLED(MyOLED.Text)
    elif state == "OFF" and MyOLED.CurrentState != "OFF":
        MyOLED.Text = "Monitor is OFF"
        MyOLED.CurrentState = "OFF"
        print_OLED(MyOLED.Text)
        
def print_OLED(text):
    
    # Clear display.
    oled.fill(0)
    oled.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))
    
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    
    # Load default font.
    font = ImageFont.load_default()
    
    # Draw Some Text
    #text = "OK"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    
    # Display image
    oled.image(image)
    oled.show()

def emergency_stop_M112():
    # uses M112 marlin command
    # Used for emergency stopping, M112 shuts down the machine, 
    # turns off all the steppers and heaters. 
    # A reset is required to return to operational mode.
    
    ser.write(b"M112\n")
    time.sleep(0.1)
    print("Used command <M112>")

def play_tone_M300():
    # uses M300 marlin command
    # Play tone - require speaker to playtones - not just beeps
    # need beep duration and frequency parameters
    
    #command = "M300 "+"S" + str(duration) + " P" + str(frequency) + "\n"
    ser.write(b"M300\n")
    time.sleep(1)
    while ser.in_waiting < 2:
        time.sleep(0.01)
    line = ser.readline().decode('utf-8').rstrip()
    if line == "ok":
        print("Used command <M300>")

def auto_home_G28():
    # uses G28 marlin command
    # Auto home all axes
    ser.write(b"G28\n")
    time.sleep(0.1)
    print("Used command <G28>")


def get_temp_M105():
    # uses M105 marlin command (need global serial variable "ser")
    # returns tuple of:
    # current printhead temperature
    # destination printhead temperature
    # current printbed temperature
    # destination printbed temperature

    ser.write(b"M105\n")
    print("Used command <M105>")
    time.sleep(0.1)
  
    head_curr_temp = 0
    head_dest_temp = 0
    bed_curr_temp = 0
    bed_dest_temp = 0
  
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

    return float(head_curr_temp), float(head_dest_temp), float(bed_curr_temp), float(bed_dest_temp)


def get_temp_hum_SI7021():
    #Returns tuple of float value of Temperature and Humidity
    #SI7021 address = 0x40
    #Read temp - No-hold master mode (no clock stretching) = 0xF3
    
    temp_raw = bytearray(2)
    hum_raw = bytearray(2)
    
    i2c.writeto(0x40, bytes([0xF3]), stop=False) 
    time.sleep(0.1)
    i2c.readfrom_into(0x40, temp_raw)
    #i2c.writeto_then_readfrom(0x40, bytes([0xF3]), temp_raw, stop=False) #Cannot use because of NACK - causes error
    
    temp_raw_int = temp_raw[0] * 256 + temp_raw[1]
    temperature = ((175.72 * temp_raw_int)/65536)-48.85
    
    i2c.writeto(0x40, bytes([0xF5]), stop=False) 
    time.sleep(0.1)
    i2c.readfrom_into(0x40, hum_raw)
    hum_raw_int = hum_raw[0] * 256 + hum_raw[1]
    humidity = ((125 * hum_raw_int)/65536)-6
    
    return round(temperature, 2), round(humidity, 2)

def get_temp_hum_AHT31():
    #Returns tuple of float value of Temperature and Humidity
    #SHT31 address = 0x44
    #CRC not used
    #2 bytes 0x24 and 0x16 means quick measurment with no clock stretching
    
    i2c.writeto(0x44, bytearray([0x24, 0x16]), stop=False) 
    
    temp_hum_raw = bytearray(6)
    time.sleep(0.1)
    
    i2c.readfrom_into(0x44, temp_hum_raw)
    
    temperature = temp_hum_raw[0] * 256 + temp_hum_raw[1]
    temperature = (175 * temperature / 65535) - 45
    
    humidity = 100 * (temp_hum_raw[3] * 256 + temp_hum_raw[4]) / 65535
    
    return round(temperature, 2), round(humidity, 2)

def get_temp_press_BMP280():
    
    sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address = 0x76)
    
    return round(sensor.temperature, 2), round(sensor.pressure, 2)


def main(args):
    
    # Clear display.
    oled.fill(0)
    oled.show()

  
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (oled.width, oled.height))
    
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    
    # Load default font.
    font = ImageFont.load_default()
    
    # Draw Some Text
    text = "RASPRINTER"
    (font_width, font_height) = font.getsize(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )
    
    # Display image
    oled.image(image)
    oled.show()
      
    
    while True:
        print('--------RASPRINTER--------')
        print('0. Zakończ program')
        print('1. Odczyt temperatur drukarki')
        print('2. Odczyt temperatur SI7021')
        option = input('wpisz numer opcji: ')
        if option == '0':
            return 0
        elif option == '1':
            hct, hdt, bct, bdt = get_temp_M105()
            print("\nbiezaca temperatura glowicy: " + str(hct))
            print("docelowa temperatura glowicy: " + str(hdt))
            print("biezaca temperatura stolu: " + str(bct))
            print("docelowa temperatura stolu: " + str(bdt))
        elif option == '2':
            print('temperatura SI7021:')
            print("%.2f°C" % round(get_temp_SI7021(), 2))
            #print(get_temp_SI7021())
        else:
            print("bledny wybor!")
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

#ok T:22.81 /0.00 B:22.66 /0.00 @:0 B@:0
