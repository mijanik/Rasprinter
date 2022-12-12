from flask import Flask, render_template, redirect, url_for, Response
from raspfunc import emergency_stop_M112, play_tone_M300, init_IO, set_relay
from sensor_database import MySensors, MyData, MyWebVariables
import threading
from monitor import MainMonitor
from camera_pi import Camera, gen
from turbo_flask import Turbo
import time


app = Flask(__name__)
turbo = Turbo(app)

@app.route('/')
def index():
    
    # If monitor is OFF - make a measurment and update charts
    if MySensors.MonitorRunningFlag == 0: 
        MySensors.ReadSensors()
        MyData.UpdateData()

    return render_template('index.html', var = MyWebVariables.WebDict())
    
def update_load():
    with app.app_context():
        while True:
            time.sleep(5) # Refresh Chart and Panel every 5 seconds
            turbo.push(turbo.replace(render_template('panel.html', var = MyWebVariables.WebDict()), 
                                     'center_panel'))
            
            turbo.push(turbo.replace(render_template('chart.html', var = MyWebVariables.WebDict()), 
                                     'center_chart'))

@app.before_first_request
def before_first_request():
    
    init_IO()
    print("Finished Initialization")
    
    threading.Thread(target=MainMonitor).start()
    print("Started Monitor")
    
    threading.Thread(target=update_load).start()
    print("Started TurboFlask")

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

@app.route('/POWER_ON')
def power_on():
    set_relay("ON")
    return redirect(url_for('index'))

@app.route('/POWER_OFF')
def power_off():
    set_relay("OFF")
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
    threading.Thread(target=lambda: app.run(host='192.168.100.76', 
                                            port=5000, debug=True, 
                                            use_reloader=False)).start()
    