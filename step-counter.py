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
data_time = []
t = 0
# Set the period of time to read the acceleration
frequency = 1000
period = 1 / frequency

def read_acceleration(num_points, t):
    while True:
        # Read acceleration
        x_acceleration = 0
        y_acceleration = 0
        z_acceleration = 0
        x_acceleration, y_acceleration, z_acceleration = mpu.acceleration
        acceleration = math.sqrt(x_acceleration ** 2 + y_acceleration ** 2 + z_acceleration ** 2)
        data_acceleration.append(acceleration)
        data_time.append(t)
        time.sleep(period)
        t += period
        if len(data_acceleration) == num_points:
            break
    return data_acceleration, data_time

# Create list to store the derivative of the acceleration
derivative_acceleration = []

def calculate_derivative(data_acceleration):
    derivative_acceleration = np.diff(data_acceleration) / period
    return derivative_acceleration

# Find minimums and maximums
local_minimums = []
local_maximums = []
time_minimums = []
time_maximums = []

def find_minimums_maximums(derivative_acceleration):
    for i in range(1, len(derivative_acceleration) - 1):
        if derivative_acceleration[i] < derivative_acceleration[i - 1] and derivative_acceleration[i] < derivative_acceleration[i + 1]:
            local_minimums.append(derivative_acceleration[i])
            time_minimums.append(data_time[i])
        elif derivative_acceleration[i] > derivative_acceleration[i - 1] and derivative_acceleration[i] > derivative_acceleration[i + 1]:
            local_maximums.append(derivative_acceleration[i])
            time_maximums.append(data_time[i])
            
    return local_minimums, local_maximums, time_minimums, time_maximums

# Main loop
num_steps = 0
all_data_acceleration = []
all_derivative_acceleration = []
all_minimums = []
all_minimum_times = []
all_maximums = []
all_maximum_times = []

while True:
    num_points = 100
    read_acceleration(num_points, t)
    all_data_acceleration.append(data_acceleration)
    derivative_acceleration = calculate_derivative(data_acceleration)
    all_derivative_acceleration.append(derivative_acceleration)
    local_minimums, local_maximums, all_minimum_times, all_maximum_times = find_minimums_maximums(derivative_acceleration)
    all_minimums.append(local_minimums)
    all_maximums.append(local_maximums)
    # print local minimums and maximums
    print("Local minimums: ", local_minimums)
    print("Local maximums: ", local_maximums)
    if len(local_minimums) > 0:
        num_steps += 1
        print("Number of steps: ", num_steps)
    if len(local_maximums) > 0:
        num_steps += 1
        print("Number of steps: ", num_steps)
    plt.plot(data_time, all_data_acceleration, 'r--', data_time, all_derivative_acceleration, 'b--', all_minimum_times, all_minimums, 'go', all_maximum_times, all_maximums, 'bo')
    plt
    data_acceleration = []
    derivative_acceleration = []
    local_minimums = []
    local_maximums = []
    time_minimums = []
    time_maximums = []