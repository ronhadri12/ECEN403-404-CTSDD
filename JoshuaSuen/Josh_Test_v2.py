# Far field of 10 meters
# 11 points at 12 degree separation (phi)
#

from dronekit import connect, VehicleMode, time, LocationGlobal
from Ron_Stuff import Rons_Stuff
from Heading_to_unit_circle import Heading_to_unit_circle
import math
import measurements as data

# Location to export data
file_path = data.filePath()
print("Exporting data to: %s" % file_path)

antenna_frequency = float(input("Antenna Frequency: "))


far_field = 10
number_paths = 1
number_points = 11


# Connect to the vehicle, perform checks, and give control of drone to user
print("Connecting to a vehicle on: /dev/ttyS0")
vehicle = connect('/dev/ttyS0',wait_ready = True, baud = 921600)	#Checks to see if the drone has booted, has GPS fix, and
																		#comleted pre-arm


heading = vehicle.heading					#sets compass heading of drone at antenna
alt_ant = vehicle.location.global_frame.alt	#sets antenna altitude

degree = Heading_to_unit_circle(heading)


for i in range(0,11,1):                                                  # runs through 11 times, once per point
    data.saveSignal(antenna_frequency, file_path)
    time.sleep(15)


output_list = Rons_Stuff(far_field, number_points, alt_ant, number_points, degree)
