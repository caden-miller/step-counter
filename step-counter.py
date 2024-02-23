import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math
import adafruit_mpu6050 as mpu6050
import time
import board
import busio

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
mpu = mpu6050.MPU6050(i2c)

# Create a list to store the data
data_acceleration = []

# Set the period of time to read the acceleration
frequency = 1000
period = 1 / frequency

while True:
    # Read acceleration
    acceleration = mpu.acceleration
    data_acceleration.append(acceleration)
    time.sleep(period)
    if len(data_acceleration) == 100:
        break

derivative_acceleration = []
