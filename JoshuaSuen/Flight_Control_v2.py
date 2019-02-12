# The following is used for controlling a Hexacopter using a
# Raspberry Pi 3 Model B (RP3) and a Pixhawk 2.4.8, using Dronekit(Mavlink)


# Import Dronekit-Python
from dronekit import connect, VehicleMode, time, LocationGlobal
import math

# Import functions
import Point_set_func_v1 as bt   # bt for Blake Thompson
import measurements_v1_1 as data   # js for Joshua Suen

import os
import sys




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
                drive_name = raw_input("Please enter the name of the external drive: ")
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

# Confirmation
print("Exporting data to: %s" % file_path)


# User input values
antenna_frequency = float(input("Antenna Frequency: "))

antenna_length = float(input("Antenna length: "))

wavelength = float(( 3 * (10 ** 8)) / antenna_frequency)

far_field = float((2 * (antenna_length ** 2)) / wavelength) # Far field calculation for antenna

number_points = input("Number of points (MUST be odd number): ")        # MUST be an odd number, to satisfy 'range' used in GPS_Coords function
while number_points < 2:
    print("Minimum number of 2 points required.")
    number_points =  input("Number of points: ")
while number_points % 2 == 0:
    print("Number of points must be odd.")
    number_points = input("Number of points: ")

########################################################################################################
# Connect to the vehicle, perform checks, take off and hold at altitude
print("Connecting to a vehicle on: /dev/ttyS0")
vehicle = connect('/dev/ttyS0',wait_ready = True, baud = 921600)	#Checks to see if the drone has booted, has GPS fix, and
																		#comleted pre-arm



#while not vehicle.is_armable:
#	print "Waiting for vehicle to initialize..."
#	time.sleep(1)



while not vehicle.channels['5'] >= 1200:
	print("Turn on manual mode(Flight Mode Switch = 1): Current Flight Mode Switch = 0")
	time.sleep(1)

# Flight Mode Switch position 2 = Guided Mode
# Flight Mode Switch position 1 = Manual Mode
# Flight Mode Switch position 0 = Manual Mode and capture GPS location of antenna

print("Mode: %s") %vehicle.mode.name

while not vehicle.armed:				#waits for vehicle to be armed
	vehicle.armed = True
	time.sleep(1)


print("Armed: %s") %vehicle.armed
time.sleep(2)



vehicle.mode = VehicleMode("STABILIZE")		#enables user control

print("Stabilize")

############################################################################################
# Manual Flight

while vehicle.channels['5'] >= 1200:		#if Flight Mode = 0 or 1 on controller, it is in manual flight

	# A switch on the remote will be used to toggle drone being controlled
	# by the user or the Raspberry Pi
    print("out loop")

    while vehicle.channels['5'] > 1600:		#if Flight Mode = 0 on controller, it is gathering antenna coordinates
	lat_ant = vehicle.location.global_frame.lat	#sets antenna latitude
	long_ant = vehicle.location.global_frame.lon	#sets antenna londitude
	alt_ant = vehicle.location.global_frame.alt	#sets antenna altitude
	heading = vehicle.heading					#sets compass heading of drone at antenna
        print("out loop")      
print(heading)
print(lat_ant)
print(long_ant)
print(alt_ant)
print(far_field)


if heading > 120 and heading <=240:
	degree_left = heading - 120 			# heading for far left of pattern (starting facing the antenna)
	degree_right = heading + 120			# heading for far right of pattern (starting facing the antenna)
elif heading < 120:							# vehicle.heading has a range of 0-360
	degree_left = 360 - (120 - heading)
	degree_right = heading + 120
elif heading > 240:
	degree_left = heading - 120
	degree_right = (heading + 120) - 360


new_degree_left = bt.Heading_to_unit_circle(degree_left)       # Converts left most degree of travel from compass heading to unit circle angle
new_degree_right = bt.Heading_to_unit_circle(degree_right)     # Converts right most degree of travel from compass heading to unit circle angle


GPS_Coord_List = bt.GPS_Coords(far_field, heading, lat_ant, long_ant, alt_ant, number_points) # Uses GPS_Coords function to calculate all points to fly to

print("Got Coordinates")
print(GPS_Coord_List)

velocity = float(0.5)							# Determines how fast the drone will fly
time_wait_1 = (far_field / velocity) + 0.5		# Calculates time (seconds) before next command is issued so drone can get to next location
point_1 = GPS_Coord_List[0]                     # Extractst the first point from the list of GPS coordinates
lat1 = point_1[0]                               # Extracts the latidude of the first coordinate
long1 = point_1[1]                              # Extracts the latidude of the first coordinate
alt1 = point_1[2]                               # Extracts the altitude of the first coordinate
################################################################################################
# Autonomous Flight

vehicle.mode = VehicleMode("GUIDED")
vehicle.mode = VehicleMode("GUIDED")
vehicle.mode = VehicleMode("GUIDED")
for i in range(1,20,1):
    print(vehicle.mode.name)

while vehicle.channels['5'] < 1200:		# If Flight Mode = 2 on controller, it is in autonomous mode

    if vehicle.channels['5'] >=  1200:
        break

	vehicle.simple_goto(LocationGlobal(lat1, long1, alt1), groundspeed = velocity)	# Commands the drone to go the the desired location at 0.5 m/s
	time.sleep(time_wait_1)

    if vehicle.channels['5'] >=  1200:
        break

    degree = 120 / (number_points - 1)  # Angle between each point (for path 1), referenced from antenna
    p1x_1 = far_field * math.sin(60)	#l ines 228-235 are used to find the necessary distance to travel to next point on the first arc
    p1y_1 = far_field * math.cos(60)
    p2x_1 = far_field * math.sin(60 - degree)
    p2y_1 = far_field * math.cos(60 - degree)
    delta_x_1 = p2x_1 - p1x_1
    delta_y_1 = p2y_1 - p1y_1
    distance_change_1 = math.sqrt(delta_x_1 ** 2 + delta_y_1 ** 2)
    time_wait_2 = (distance_change_1 / velocity) + 0.5    # Calculates time before next command is issued so drone can get to next location

    print("test_1")


    for i in range(1,number_points,1):	# Iterates through and travels to specified number of points
        if vehicle.channels['5'] >=  1200:
            break
	current_point = GPS_Coord_List[i]         # Extracts next GPS Location to go to from GPS_Coord_List
	lat_loop = current_point[0]               # Extracts the latidude of the next coordinate
	long_loop = current_point[1]              # Extracts the latidude of the next coordinate
        alt_loop = current_point[2]               # Extracts the altitude of the next coordinate

	vehicle.simple_goto(LocationGlobal(lat_loop, long_loop, alt_loop),groundspeed = velocity)

        for t in range(1,int(math.ceil(time_wait_2)) * 2, 1):     # Continuously checks for operator overrride to return to manual control
            if vehicle.channels['5'] >=  1200:
                break
            time.sleep(0.5)

    print("test_2")

    for t in range(1,10, 1):                      # Drone waits for operator to take control once it has completed the path
        if vehicle.channels['5'] >=  1200:
            break
        time.sleep(0.5)

    print("test_3")
############################################################################################
# Manual Control
vehicle.mode = VehicleMode("STABILIZE")
vehicle.mode = VehicleMode("STABILIZE")
vehicle.mode = VehicleMode("STABILIZE")		# Returns control back to user, in case of malfunction or end of flight path
print("test_4")