from flask import Flask, render_template, redirect, url_for
from raspfunc import get_temp_M105, get_temp_hum_SI7021, get_temp_hum_AHT31, get_temp_press_BMP280, set_LED
from sensor_database import *
import threading
from monitor import MainMonitor

app = Flask(__name__)



@app.route('/')
def index():
    hct, hdt, bct, bdt = get_temp_M105()
    t1, h1 = get_temp_hum_SI7021()
    t2, h2 = get_temp_hum_AHT31()
    t3, p3 = get_temp_press_BMP280()
    return render_template('index.html', nozzle_temp=hct, target_nozzle_temp=hdt, bed_temp = bct, target_bed_temp = bdt, si7021_temp = t1, si7021_hum = h1, AHT31_temp = t2, AHT31_hum = h2, BMP280_temp = t3, BMP280_press = p3)

@app.route('/RED_ON')
def red_on():
    set_LED('RED', 'ON')
    return redirect(url_for('index'))
    
@app.route('/GREEN_ON')
def green_on():
    set_LED('GREEN', 'ON')
    return redirect(url_for('index'))
    
@app.route('/BLUE_ON')
def blue_on():
    set_LED('BLUE', 'ON')
    return redirect(url_for('index'))
    
@app.route('/ALL_OFF')
def all_off():
    set_LED('RED', 'OFF')
    set_LED('GREEN', 'OFF')
    set_LED('BLUE', 'OFF')
    return redirect(url_for('index'))

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
    #app.run(debug=True, host='192.168.100.76')
    threading.Thread(target=lambda: app.run(host='192.168.100.76', port=5000, debug=True, use_reloader=False)).start()
    print("Started Flask Thread")
    threading.Thread(target=MainMonitor).start()
    print("Started Monitor")