from raspfunc import get_temp_M105, get_temp_hum_HTU21D, get_temp_hum_SHT31, get_temp_press_BMP280
import numpy as np
from enum import Enum

class SensorDatabase:
    def __init__(self):
        self.MonitorRunningFlag = 0
        
        #Sensors inside a printer
        self.PrintheadCurrentTemp = 0.0
        self.PrintheadTargetTemp = 0.0
        self.PrintbedCurrentTemp = 0.0
        self.PrintbedTargetTemp = 0.0
        
        #External sensors
        self.HTU21DTemp = 0.0
        self.HTU21DHum = 0.0
        self.SHT31Temp = 0.0
        self.SHT31Hum = 0.0
        self.BMP280Temp = 0.0
        self.BMP280Pres = 0.0
    
    def ReadSensors(self):
        self.PrintheadCurrentTemp, self.PrintheadTargetTemp, \
        self.PrintbedCurrentTemp, self.PrintbedTargetTemp = get_temp_M105()
        
        self.HTU21DTemp, self.HTU21DHum = get_temp_hum_HTU21D()
        self.SHT31Temp, self.SHT31Hum = get_temp_hum_SHT31()
        self.BMP280Temp, self.BMP280Pres = get_temp_press_BMP280()

MySensors = SensorDatabase()

class DataBuffer:
    def __init__(self):
        #7 sensors - 7 arrays
        self.PrintheadCurrentTemp = np.zeros(20)
        self.PrintheadTargetTemp = np.zeros(20)
        self.PrintbedCurrentTemp = np.zeros(20)
        self.PrintbedTargetTemp = np.zeros(20)
        self.HTU21DTemp = np.zeros(20)
        self.SHT31Temp = np.zeros(20)
        self.BMP280Temp = np.zeros(20)
        
        self.labels = np.arange(20)
        
    def UpdateData(self):
        #shift to right measurements
        self.PrintheadCurrentTemp = np.roll(self.PrintheadCurrentTemp, 1)
        self.PrintheadTargetTemp = np.roll(self.PrintheadTargetTemp, 1)
        self.PrintbedCurrentTemp = np.roll(self.PrintbedCurrentTemp, 1)
        self.PrintbedTargetTemp = np.roll(self.PrintbedTargetTemp, 1) 
        self.HTU21DTemp = np.roll(self.HTU21DTemp, 1) 
        self.SHT31Temp = np.roll(self.SHT31Temp, 1)
        self.BMP280Temp = np.roll(self.BMP280Temp, 1) 
        
        #overwrite first element
        self.PrintheadCurrentTemp[0] = MySensors.PrintheadCurrentTemp
        self.PrintheadTargetTemp[0] = MySensors.PrintheadTargetTemp
        self.PrintbedCurrentTemp[0] = MySensors.PrintbedCurrentTemp
        self.PrintbedTargetTemp[0] = MySensors.PrintbedTargetTemp
        self.HTU21DTemp[0] = MySensors.HTU21DTemp
        self.SHT31Temp[0] = MySensors.SHT31Temp
        self.BMP280Temp[0] = MySensors.BMP280Temp
            
MyData = DataBuffer()

class SensorErrorCode(Enum):
    PrintheadCurrentTemp = 1
    PrintbedCurrentTemp = 2
    HTU21DTemp = 3
    SHT31Temp = 4
    BMP280Temp = 5

class WebpageVariables:
    
    def __init__(self):
        self.webpage_variables = {
        'printhead_temp' : 0,
        'target_printhead_temp' : 0,
        'bed_temp' : 0,
        'target_bed_temp' : 0,
        'HTU21D_temp' : 0, 
        'HTU21D_hum' : 0,
        'SHT31_temp' : 0, 
        'SHT31_hum' : 0,
        'BMP280_temp' : 0, 
        'BMP280_press' : 0,
        'MonitorRunningFlag' : 0,
        'labels' : 0,
        'PrintheadCurrentTempData' : 0,
        'PrintbedCurrentTempData' : 0,
        'PrintheadTargetTempData' : 0,
        'PrintbedTargetTempData' : 0,
        'HTU21DTempData' : 0,
        'SHT31TempData' : 0,
        'BMP280TempData' : 0
        }
    
    def UpdateVariables(self):
        self.webpage_variables.update({
        'printhead_temp' : MySensors.PrintheadCurrentTemp,
        'target_printhead_temp' : MySensors.PrintheadTargetTemp,
        'bed_temp' : MySensors.PrintbedCurrentTemp,
        'target_bed_temp' : MySensors.PrintbedTargetTemp,
        'HTU21D_temp' : MySensors.HTU21DTemp, 
        'HTU21D_hum' : MySensors.HTU21DHum,
        'SHT31_temp' : MySensors.SHT31Temp, 
        'SHT31_hum' : MySensors.SHT31Hum,
        'BMP280_temp' : MySensors.BMP280Temp, 
        'BMP280_press' : MySensors.BMP280Pres,
        'MonitorRunningFlag' : MySensors.MonitorRunningFlag,
        'labels' : MyData.labels,
        'PrintheadCurrentTempData' : MyData.PrintheadCurrentTemp,
        'PrintbedCurrentTempData' : MyData.PrintbedCurrentTemp,
        'PrintheadTargetTempData' : MyData.PrintheadTargetTemp,
        'PrintbedTargetTempData' : MyData.PrintbedTargetTemp,
        'HTU21DTempData' : MyData.HTU21DTemp,
        'SHT31TempData' : MyData.SHT31Temp,
        'BMP280TempData' : MyData.BMP280Temp
        })
        
    def WebDict(self):
        self.UpdateVariables()
        return self.webpage_variables
    
MyWebVariables = WebpageVariables()
