class SensorDatabase:
    MonitorRunningFlag = 0
    
    #Sensors inside a printer
    PrintheadCurrentTemp = 0.0
    PrintheadTargetTemp = 0.0
    PrintbedCurrentTemp = 0.0
    PrintbedTargetTemp = 0.0
    
    #External sensors
    SI7021Temp = 0.0
    SI7021Hum = 0.0
    AHT31Temp = 0.0
    AHT31Hum = 0.0
    BMP280Temp = 0.0
    BMP280Pres = 0.0
    
MySensors = SensorDatabase()