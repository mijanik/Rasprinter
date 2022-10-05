from raspfunc import get_temp_M105, get_temp_hum_SI7021, get_temp_hum_AHT31, get_temp_press_BMP280
import numpy as np
class SensorDatabase:
    def __init__(self):
        self.MonitorRunningFlag = 0
        
        #Sensors inside a printer
        self.PrintheadCurrentTemp = 0.0
        self.PrintheadTargetTemp = 0.0
        self.PrintbedCurrentTemp = 0.0
        self.PrintbedTargetTemp = 0.0
        
        #External sensors
        self.SI7021Temp = 0.0
        self.SI7021Hum = 0.0
        self.AHT31Temp = 0.0
        self.AHT31Hum = 0.0
        self.BMP280Temp = 0.0
        self.BMP280Pres = 0.0
    
    def ReadSensors(self):
        self.PrintheadCurrentTemp, self.PrintheadTargetTemp, self.PrintbedCurrentTemp, self.PrintbedTargetTemp = get_temp_M105()
        self.SI7021Temp, self.SI7021Hum = get_temp_hum_SI7021()
        self.AHT31Temp, self.AHT31Hum = get_temp_hum_AHT31()
        self.BMP280Temp, self.BMP280Pres = get_temp_press_BMP280()

MySensors = SensorDatabase()

class DataBuffer:
    def __init__(self):
        rows = 7 #7 temperature sensors
        columns = 20
        data = np.zeros([rows, columns])

    def UpdateData(self):
        self.data[0, 0] = MySensors.PrintheadCurrentTemp
        self.data[1, 0] = MySensors.PrintheadTargetTemp
        self.data[1, 0] = MySensors.PrintheadTargetTemp
        self.data[1, 0] = MySensors.PrintheadTargetTemp
        self.data[1, 0] = MySensors.PrintheadTargetTemp
        self.data[1, 0] = MySensors.PrintheadTargetTemp
        self.data[1, 0] = MySensors.PrintheadTargetTemp
            

