# Far field of 10 meters
# 11 points at 12 degree separation (phi)
#

from dronekit import connect, VehicleMode, time, LocationGlobal
from Ron_Stuff import Rons_Stuff
from Heading_to_unit_circle import Heading_to_unit_circle
import math
import os
import measurements as data

# Location to export data
while True:
    storage = input("Where do you want to export the data?"
                    "\n[1] Onboard storage \n[2] External drive \n")
    # Onboard storage
    if storage == 1:
        file_path = "/home/pi"
    # External drive
    elif storage == 2:
        drive_name = raw_input("Please enter the name of the external drive: ")
        file_path = "/media/pi/" + drive_name
        # Check for specified external drive
        while os.path.exists(file_path) != True:
            drive_name = raw_input("The file path %s not exist. Export data "
                                   "to onboard storage? [Y/N] " % file_path)
            if drive_name == "Y" or drive_name == "y":
                file_path = "/home/pi"
                break
            elif drive_name == "N" or drive_name == "n":
                drive_name = raw_input("\nPlease enter the name of the external drive: ")
                file_path = "/media/pi/" + drive_name
            else:
                print("Please enter [Y] or [N].")
    else:
        print("Please enter [1] or [2].\n")

    # Confirm save location
    confirm = raw_input("Data will be exported to: %s [Y/N] " % file_path)

    if confirm == "Y" or confirm == "y":
        break
    elif confirm == "N" or confirm == "n":
        continue
    else:
        print("Error: Inavlid input")

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

    #Insert gain code here
    time.sleep(15)


output_list = Rons_Stuff(far_field, number_points, alt_ant, number_points, degree)
