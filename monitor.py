from sensor_database import *
import time
from raspfunc import set_LED, show_status_OK

def MainMonitor():
    
    BlinkSecondsTimestamp = 0.0
    LEDStatus = 0
    
    set_LED('GREEN', 'ON')
    show_status_OK()
    while 1:
        if MySensors.MonitorRunningFlag == 1:
            CurrentSeconds = time.time()
            if CurrentSeconds >= BlinkSecondsTimestamp + 1:
                set_LED('RED', LEDStatus)
                LEDStatus ^= 1
                BlinkSecondsTimestamp = CurrentSeconds

    
if __name__ == "__main__":
    pass