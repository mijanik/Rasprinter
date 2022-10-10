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
        #7 sensors - 7 arrays
        self.PrintheadCurrentTemp = np.zeros(20)
        self.PrintheadTargetTemp = np.zeros(20)
        self.PrintbedCurrentTemp = np.zeros(20)
        self.PrintbedTargetTemp = np.zeros(20)
        self.SI7021Temp = np.zeros(20)
        self.AHT31Temp = np.zeros(20)
        self.BMP280Temp = np.zeros(20)
        
        self.labels = np.arange(20)
        
    def UpdateData(self):
        #shift to right measurements
        self.PrintheadCurrentTemp = np.roll(self.PrintheadCurrentTemp, 1)
        self.PrintheadTargetTemp = np.roll(self.PrintheadTargetTemp, 1)
        self.PrintbedCurrentTemp = np.roll(self.PrintbedCurrentTemp, 1)
        self.PrintbedTargetTemp = np.roll(self.PrintbedTargetTemp, 1) 
        self.SI7021Temp = np.roll(self.SI7021Temp, 1) 
        self.AHT31Temp = np.roll(self.AHT31Temp, 1)
        self.BMP280Temp = np.roll(self.BMP280Temp, 1) 
        
        #overwrite first element
        self.PrintheadCurrentTemp[0] = MySensors.PrintheadCurrentTemp
        self.PrintheadTargetTemp[0] = MySensors.PrintheadTargetTemp
        self.PrintbedCurrentTemp[0] = MySensors.PrintbedCurrentTemp
        self.PrintbedTargetTemp[0] = MySensors.PrintbedTargetTemp
        self.SI7021Temp[0] = MySensors.SI7021Temp
        self.AHT31Temp[0] = MySensors.AHT31Temp
        self.BMP280Temp[0] = MySensors.BMP280Temp
            
MyData = DataBuffer()

if __name__ == '__main__':
    pass