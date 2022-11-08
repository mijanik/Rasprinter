from flask import Flask, render_template, redirect, url_for, Response
from raspfunc import emergency_stop_M112, play_tone_M300
from sensor_database import *
import threading
from monitor import MainMonitor
from camera_pi import Camera, gen
from turbo_flask import Turbo
import time

app = Flask(__name__)
turbo = Turbo(app)

@app.route('/')
def index():
    if MySensors.MonitorRunningFlag == 0:
        MySensors.ReadSensors()
        MyData.UpdateData()

    return render_template('index.html', nozzle_temp=MySensors.PrintheadCurrentTemp, 
                           target_nozzle_temp=MySensors.PrintheadTargetTemp, 
                           bed_temp = MySensors.PrintbedCurrentTemp, 
                           target_bed_temp = MySensors.PrintbedTargetTemp, 
                           si7021_temp = MySensors.SI7021Temp, si7021_hum = MySensors.SI7021Hum, 
                           AHT31_temp = MySensors.AHT31Temp, AHT31_hum = MySensors.AHT31Hum, 
                           BMP280_temp = MySensors.BMP280Temp, BMP280_press = MySensors.BMP280Pres, 
                           MonitorRunningFlag = MySensors.MonitorRunningFlag,
                           labels = MyData.labels,
                           PrintheadCurrentTempData = MyData.PrintheadCurrentTemp,
                           PrintbedCurrentTempData = MyData.PrintbedCurrentTemp,
                           PrintheadTargetTempData = MyData.PrintheadTargetTemp,
                           PrintbedTargetTempData = MyData.PrintbedTargetTemp)
    
def update_load():
    with app.app_context():
        while True:
            time.sleep(1)
            turbo.push(turbo.replace(render_template('panel.html', nozzle_temp=MySensors.PrintheadCurrentTemp, 
                           target_nozzle_temp=MySensors.PrintheadTargetTemp, 
                           bed_temp = MySensors.PrintbedCurrentTemp, 
                           target_bed_temp = MySensors.PrintbedTargetTemp, 
                           si7021_temp = MySensors.SI7021Temp, si7021_hum = MySensors.SI7021Hum, 
                           AHT31_temp = MySensors.AHT31Temp, AHT31_hum = MySensors.AHT31Hum, 
                           BMP280_temp = MySensors.BMP280Temp, BMP280_press = MySensors.BMP280Pres, 
                           MonitorRunningFlag = MySensors.MonitorRunningFlag), 'center_panel'))
            
            turbo.push(turbo.replace(render_template('chart.html', labels = MyData.labels,
                           PrintheadCurrentTempData = MyData.PrintheadCurrentTemp,
                           PrintbedCurrentTempData = MyData.PrintbedCurrentTemp,
                           PrintheadTargetTempData = MyData.PrintheadTargetTemp,
                           PrintbedTargetTempData = MyData.PrintbedTargetTemp), 'center_chart'))

@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()
    



@app.route('/TOGGLE_MONITOR')
def toggle_monitor():
    MySensors.MonitorRunningFlag ^= 1
    return redirect(url_for('index'))

@app.route('/EMERGENCY_STOP')
def emergency_stop():
    emergency_stop_M112()
    return redirect(url_for('index'))

@app.route('/BEEP')
def beep():
    play_tone_M300()
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.config['SERVER_NAME'] = "192.168.100.76:5000"

    threading.Thread(target=lambda: app.run(host='192.168.100.76', port=5000, debug=True, use_reloader=False)).start()
    print("Started Flask Thread")
    threading.Thread(target=MainMonitor).start()
    print("Started Monitor")