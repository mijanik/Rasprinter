from sensor_database import MySensors, MyData


class WebpageVariables:
    
    def __init__(self):
        self.webpage_variables = {
        'nozzle_temp' : 0,
        'target_nozzle_temp' : 0,
        'bed_temp' : 0,
        'target_bed_temp' : 0,
        'si7021_temp' : 0, 
        'si7021_hum' : 0,
        'AHT31_temp' : 0, 
        'AHT31_hum' : 0,
        'BMP280_temp' : 0, 
        'BMP280_press' : 0,
        'MonitorRunningFlag' : 0,
        'labels' : 0,
        'PrintheadCurrentTempData' : 0,
        'PrintbedCurrentTempData' : 0,
        'PrintheadTargetTempData' : 0,
        'PrintbedTargetTempData' : 0
        }
    
    def UpdateVariables(self):
        self.webpage_variables.update({
        'nozzle_temp' : MySensors.PrintheadCurrentTemp,
        'target_nozzle_temp' : MySensors.PrintheadTargetTemp,
        'bed_temp' : MySensors.PrintbedCurrentTemp,
        'target_bed_temp' : MySensors.PrintbedTargetTemp,
        'si7021_temp' : MySensors.SI7021Temp, 
        'si7021_hum' : MySensors.SI7021Hum,
        'AHT31_temp' : MySensors.AHT31Temp, 
        'AHT31_hum' : MySensors.AHT31Hum,
        'BMP280_temp' : MySensors.BMP280Temp, 
        'BMP280_press' : MySensors.BMP280Pres,
        'MonitorRunningFlag' : MySensors.MonitorRunningFlag,
        'labels' : MyData.labels,
        'PrintheadCurrentTempData' : MyData.PrintheadCurrentTemp,
        'PrintbedCurrentTempData' : MyData.PrintbedCurrentTemp,
        'PrintheadTargetTempData' : MyData.PrintheadTargetTemp,
        'PrintbedTargetTempData' : MyData.PrintbedTargetTemp
        })
        
    def WebDict(self):
        self.UpdateVariables()
        return self.webpage_variables
    
MyWebVariables = WebpageVariables()