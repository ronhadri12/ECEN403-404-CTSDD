import math
import os
import measurements as data
import datetime

# Location to export data
file_path = data.filePath()

antenna_frequency = float(input("Antenna Frequency: "))


far_field = 10.47
number_paths = 3
number_points = 11

total_points = number_paths * number_points


for i in range(0,total_points,1):
    print("Starting measurements for point %d" % i)
    print(datetime.datetime.now())
    data.saveSignal(i, antenna_frequency, file_path)
    print(datetime.datetime.now())
    print("Move to next point.")