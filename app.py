from flask import Flask, render_template, redirect, url_for
import RPi.GPIO as GPIO
from raspfunc import get_temp_M105, get_temp_hum_SI7021, get_temp_hum_AHT31, get_temp_press_BMP280

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

GPIO.output(13, 0)
GPIO.output(19, 0)
GPIO.output(26, 0)

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
    GPIO.output(13, 1)
    return redirect(url_for('index'))
    
@app.route('/GREEN_ON')
def green_on():
    GPIO.output(19, 1)
    return redirect(url_for('index'))
    
@app.route('/BLUE_ON')
def blue_on():
    GPIO.output(26, 1)
    return redirect(url_for('index'))
    
@app.route('/ALL_OFF')
def all_off():
    GPIO.output(13, 0)
    GPIO.output(19, 0)
    GPIO.output(26, 0)
    return redirect(url_for('index'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, host='192.168.100.76')
