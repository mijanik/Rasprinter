from sensor_database import MySensors, MyData, SensorErrorCode
import time
from raspfunc import set_LED, status_OLED, print_OLED, play_tone_M300, set_relay

def CheckTemperaturesAbnormal():
    #Check every temperature sensor if its value is safe
    #returns 0 if OK
    
    if MySensors.PrintheadCurrentTemp > 260:
        return SensorErrorCode['PrintheadCurrentTemp'].value
    
    elif MySensors.PrintbedCurrentTemp > 100:
        return SensorErrorCode['PrintbedCurrentTemp'].value
    
    elif MySensors.HTU21DTemp > 50:
        return SensorErrorCode['HTU21DTemp'].value
    
    elif MySensors.SHT31Temp > 50:
        return SensorErrorCode['SHT31Temp'].value
    
    elif MySensors.BMP280Temp > 50:
        return SensorErrorCode['BMP280Temp'].value
    
    else:
        return 0 # All sensors OK


def MainMonitor():
    
    BlinkSecondsTimestamp = 0.0
    LEDStatus = 0
    TemperatureStatus = 0
    
    set_LED('GREEN', 'ON')
    print_OLED("RASPRINTER")
    
    # Monitoring loop
    while True:
        
        # If monitor flag is ON
        if MySensors.MonitorRunningFlag == 1:
            
            status_OLED("ON")
           
            # Toggle status LED
            set_LED('RED', LEDStatus)
            LEDStatus ^= 1                                  
        
            MySensors.ReadSensors()
            TemperatureStatus = CheckTemperaturesAbnormal()
            MyData.UpdateData()
        
            # If at least one temperature is unsafe - beep and turn printer OFF
            if TemperatureStatus != 0: 
                play_tone_M300()
                set_relay("OFF")
        
        elif MySensors.MonitorRunningFlag == 0:
            status_OLED("OFF")

        time.sleep(5)
        