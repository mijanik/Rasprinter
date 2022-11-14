from sensor_database import *
import time
from raspfunc import set_LED, status_OLED, print_OLED, play_tone_M300, set_relay

def CheckTemperaturesAbnormal():
    #Check every temperature sensor if its value is safe
    #returns 0 if OK
    
    if MySensors.PrintheadCurrentTemp > 250:
        return 1
    
    elif MySensors.PrintbedCurrentTemp > 100:
        return 2
    
    elif MySensors.SI7021Temp > 50:
        return 3
    
    elif MySensors.AHT31Temp > 50:
        return 4
    
    elif MySensors.BMP280Temp > 50:
        return 5
    
    else:
        return 0
    
    pass


def MainMonitor():
    
    BlinkSecondsTimestamp = 0.0
    LEDStatus = 0
    set_LED('GREEN', 'ON')
    print_OLED("Hello!")
    
    TemperatureStatus = 0
    
    set_relay("ON")
    time.sleep(2)
    set_relay("OFF")
    
    #Monitoring loop
    while 1:
        
        #If monitor is turned ON
        if MySensors.MonitorRunningFlag == 1:
            
            status_OLED("ON")
            
           
            CurrentSeconds = time.time()
            if CurrentSeconds >= BlinkSecondsTimestamp + 5:
                set_LED('RED', LEDStatus)
                LEDStatus ^= 1
                BlinkSecondsTimestamp = CurrentSeconds
            
                MySensors.ReadSensors()
                TemperatureStatus = CheckTemperaturesAbnormal()
                MyData.UpdateData()
            
            if TemperatureStatus != 0:
                play_tone_M300()
                
        
        elif MySensors.MonitorRunningFlag == 0:
            status_OLED("OFF")
            
            

    
if __name__ == "__main__":
    pass