from flask import Flask, render_template, redirect, url_for
#from raspfunc import get_temp_M105, get_temp_hum_SI7021, get_temp_hum_AHT31, get_temp_press_BMP280, set_LED
from sensor_database import *
import threading
from monitor import MainMonitor

app = Flask(__name__)

@app.route('/')
def index():
    #hct, hdt, bct, bdt = get_temp_M105()
    #t1, h1 = get_temp_hum_SI7021()
    #t2, h2 = get_temp_hum_AHT31()
    #t3, p3 = get_temp_press_BMP280()
    if MySensors.MonitorRunningFlag == 0:
        MySensors.ReadSensors()
    
    return render_template('index.html', nozzle_temp=MySensors.PrintheadCurrentTemp, 
                           target_nozzle_temp=MySensors.PrintheadTargetTemp, 
                           bed_temp = MySensors.PrintbedCurrentTemp, 
                           target_bed_temp = MySensors.PrintbedTargetTemp, 
                           si7021_temp = MySensors.SI7021Temp, si7021_hum = MySensors.SI7021Hum, 
                           AHT31_temp = MySensors.AHT31Temp, AHT31_hum = MySensors.AHT31Hum, 
                           BMP280_temp = MySensors.BMP280Temp, BMP280_press = MySensors.BMP280Pres, 
                           MonitorRunningFlag = MySensors.MonitorRunningFlag)


@app.route('/TOGGLE_MONITOR')
def toggle_monitor():
    print(MySensors.MonitorRunningFlag)
    MySensors.MonitorRunningFlag ^= 1
    return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':

    threading.Thread(target=lambda: app.run(host='192.168.100.76', port=5000, debug=True, use_reloader=False)).start()
    print("Started Flask Thread")
    threading.Thread(target=MainMonitor).start()
    print("Started Monitor")