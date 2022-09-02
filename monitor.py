from sensor_database import *
import time
from raspfunc import set_LED, status_OLED, print_OLED

def MainMonitor():
    
    BlinkSecondsTimestamp = 0.0
    LEDStatus = 0
    OLEDRoationFlag = 0
    set_LED('GREEN', 'ON')
    print_OLED("Hello!")
    
    
    
    #Monitoring loop
    while 1:
        
        #If monitor is turned ON
        if MySensors.MonitorRunningFlag == 1:
            
            status_OLED("ON")
            
            #Blinking RED LED
            CurrentSeconds = time.time()
            if CurrentSeconds >= BlinkSecondsTimestamp + 1:
                set_LED('RED', LEDStatus)
                LEDStatus ^= 1
                BlinkSecondsTimestamp = CurrentSeconds
            #####
            
            MySensors.ReadSensors()
            time.sleep(5)
        
        elif MySensors.MonitorRunningFlag == 0:
            status_OLED("OFF")
            
            

    
if __name__ == "__main__":
    pass