# Corsair AIO Control

Requires [Python3](https://www.python.org).\
Requires [liquidctl](https://pypi.org/project/liquidctl).

My AIO (H115i RGB Elite) doesn't work properly with some PWM fans (RS140 ARGB) connected directly to the fan headers.\
This script allows to connect radiator fans to a motherboard header and adjust their speed based on AIO coolant temperature.

Find the pwm device your fans are connected to.\
Mine is `/sys/class/hwmon/hwmon2/pwm2`.\
Use `lm_sensors`/`pwmconfig` to identify correct device.

Enable manual control of the device by writing `1` to `/sys/class/hwmon/hwmon2/pwm2_enable`.\
Disable manual control by writing `5`.

Find the driver for your AIO.\
Mine is `liquidctl.driver.hydro_platinum`.\
Parse and match devices then initialize.

Parse and match water temperature then set fan speeds.
