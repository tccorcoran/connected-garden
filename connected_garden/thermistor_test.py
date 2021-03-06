import time
import board
import adafruit_thermistor
pin = board.TEMPERATURE
resistor = 10000
resistance = 10000
nominal_temp = 25
b_coefficient = 3950

thermistor = adafruit_thermistor.Thermistor(
    pin, resistor, resistance, nominal_temp, b_coefficient
)

# print the temperature in C and F to the serial console every second
while True:
    celsius = thermistor.temperature
    fahrenheit = (celsius * 9 / 5) + 32
    print("== Temperature ==\n{} *C\n{} *F\n".format(celsius, fahrenheit))
    time.sleep(1)
