#!/usr/bin/python3

from time import sleep
from signal import signal, SIGINT, SIGTERM
from os import system
from subprocess import check_output
from liquidctl.driver.hydro_platinum import HydroPlatinum

# TempC : SpeedPWM (0-255)
curve = { 45 : 255, # 100%
          44 : 242,  # 95%
          43 : 230,  # 90%
          42 : 217,  # 85%
          41 : 204,  # 80%
          40 : 191,  # 75%
          39 : 179,  # 70%
          38 : 166,  # 65%
          37 : 153,  # 60%
          36 : 140,  # 55%
          35 : 128 } # 50%

def handle_stop_signals(signum, frame):
    disable_control()
    exit(0)

def enable_control(): system("echo 1 > /sys/class/hwmon/hwmon2/pwm2_enable")

def disable_control(): system("echo 5 > /sys/class/hwmon/hwmon2/pwm2_enable")

def set_fan_speed(speed): system(" ".join(["echo", str(speed), "> /sys/class/hwmon/hwmon2/pwm2"]))

def get_fan_speed(): return check_output("cat /sys/class/hwmon/hwmon2/pwm2", shell=True).decode().strip("\n")

def get_water_temp(device):
    status = device.get_status()
    for entry in status:
        if "Liquid temperature" in entry:
            temp = round(entry[1], 1)
            return temp
    return None

signal(SIGINT, handle_stop_signals)
signal(SIGTERM, handle_stop_signals)

def main():
    device = False
    enable_control()
    fans = get_fan_speed()
    for dev in HydroPlatinum.find_supported_devices():
        if dev.description == "Corsair iCUE H115i Elite RGB":
            device = dev
    if device is False: exit(1)
    with device.connect():
        device.initialize()
        while True:
            temp = get_water_temp(device)
            if temp is None: continue
            for key, value in curve.items():
                if temp >= key:
                    if fans != value:
                        set_fan_speed(curve[key])
                        fans = curve[key]
                    break
            sleep(1)
    disable_control()

if __name__ == "__main__":
    main()
