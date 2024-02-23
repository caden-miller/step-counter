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

def read_acceleration(num_points):
    while True:
        # Read acceleration
        acceleration = mpu.acceleration
        data_acceleration.append(acceleration)
        time.sleep(period)
        if len(data_acceleration) == num_points:
            break
    return data_acceleration

# Create list to store the derivative of the acceleration
derivative_acceleration = []

def calculate_derivative(data_acceleration):
    derivative_acceleration = np.diff(data_acceleration) / period
    return derivative_acceleration

# Find minimums and maximums
local_minimums = []
local_maximums = []

def find_minimums_maximums(derivative_acceleration):
    for i in range(1, len(derivative_acceleration) - 1):
        if derivative_acceleration[i] < derivative_acceleration[i - 1] and derivative_acceleration[i] < derivative_acceleration[i + 1]:
            local_minimums.append(derivative_acceleration[i])
        elif derivative_acceleration[i] > derivative_acceleration[i - 1] and derivative_acceleration[i] > derivative_acceleration[i + 1]:
            local_maximums.append(derivative_acceleration[i])
    return local_minimums, local_maximums

# Main loop
num_steps = 0
while True:
    num_points = 100
    read_acceleration(num_points)
    derivative_acceleration = calculate_derivative(data_acceleration)
    local_minimums, local_maximums = find_minimums_maximums(derivative_acceleration)
    # print local minimums and maximums
    print("Local minimums: ", local_minimums)
    print("Local maximums: ", local_maximums)
    if len(local_minimums) > 0:
        num_steps += 1
        print("Number of steps: ", num_steps)
    if len(local_maximums) > 0:
        num_steps += 1
        print("Number of steps: ", num_steps)