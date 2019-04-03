# Far field of 10 meters
# 11 points at 12 degree separation (phi)

from dronekit import connect, VehicleMode, time, LocationGlobal
from Ron_Stuff import Rons_Stuff
from Heading_to_unit_circle import Heading_to_unit_circle
import math
import os
import measurements as data

# Location to export data
file_path = data.filePath()

antenna_frequency = float(input("Antenna Frequency: "))


far_field = 10.47
number_paths = 3
number_points = 11

total_points = number_paths * number_points


# Connect to the vehicle, perform checks, and give control of drone to user
print("Connecting to a vehicle on: /dev/ttyS0")
vehicle = connect('/dev/ttyS0',wait_ready = True, baud = 921600)	#Checks to see if the drone has booted, has GPS fix, and
																		#comleted pre-arm


heading = vehicle.heading					#sets compass heading of drone at antenna
alt_ant = vehicle.location.global_frame.alt	#sets antenna altitude

degree = Heading_to_unit_circle(heading)


for i in range(0,total_points,1):
    print("Starting measurements for point %d" % i)
    data.saveSignal(i, antenna_frequency, file_path)
    print("Move to next point.")
    time.sleep(3)
    


#output_list = Rons_Stuff(far_field, number_points, alt_ant, number_paths, degree)