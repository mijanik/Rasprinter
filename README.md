# RASPRINTER
###### by Miłosz Janik
Google Slides - project description [PL] (20.01.2023) https://docs.google.com/presentation/d/1w7VxQLNavUgkZQrJ2IbT4koUca9OFTzJjdb9SjkVRik/edit?usp=sharing

![alt text](https://github.com/mijanik/Rasprinter/blob/master/Rasprinter_interface.png)

## Project purpose
The aim of the project was to enable monitoring (for safety reasons) of the printer's operation by measuring temperature and viewing the image from the camera.

## Project physical components
- 3D Printer - Homers Tarantula Pro with *mks sgen_l v1.0* motherboard and Marlin Firmware
- Raspberry Pi 2B
- 3x I2C temperature sensors
- Dedicated Raspberry Pi camera
- I2C OLED screen
- Multi-color LED diode
- SSR Relay + NPN-as-key circuit
## Tech Stack
- Python OOP
- Flask
- Threading
- I2C + UART
- HTML, CSS, Chart.js
- Visual Studio Code Remote Development + Git
- 3D modeling (Siemens NX) + 3D printing

## Project main functionality
- Monitor printer temperatures from built-in sensors (Printhead and Printbed) and I2C sensors
- Autonomous temperature monitoring - if they are not safe, printer will be shut down
- Show temperatures and camera preview on web page

## About project
- Developer and owner: Miłosz Janik
- Made for Diploma Engineering Thesis - Bachelor degree - "System monitorowania parametrów pracy drukarki 3D"
- Thesis promoter: PhD Agnieszka Dąbrowska-Boruch
- Field of study: Electronics and Telecommunications
- Status - Diploma thesis defended, project development suspended

