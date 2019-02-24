# The following is used for controlling a Hexacopter using a
# Raspberry Pi 3 Model B (RP3) and a Pixhawk 2.4.8, using Dronekit(Mavlink)

### FIX NAMING ###
import Ron_Stuff as ron
# Import Dronekit-Python
from dronekit import connect, VehicleMode, time, LocationGlobal
import math

# Import functions
import Point_set_func_v1 as bt   # Blake's functions
import measurements as data   # Josh's functions

# Used for opening and writing to files
from pathlib2 import Path


# Location to export data
file_path = data.filePath()

# Calculate spherical coordinates
far_field = 6.5                              # distance of points from antenna in the far field
number_points = 11                          # number of points per path
height = [0]                    # number of vertiacl meters BELOW the antenna
number_paths = 1                            # Number of paths to be run
gain = [-20, -17,-16,-15,-14,-13,-14,-15,-16,-17,-20,-10,-7,-6,-5,-4,-3,-4,-5,-6,-7,-10,-7,-4,-3,-2,-1,0,-1,-2,-3,-4,-7,-17,-14,-13,-12,-11,-10,-11,-12,-13,-14,-17]
degree = 120 / (number_points - 1)

coord_data = ron.Rons_Stuff(far_field, number_points, height, number_paths, degree)

# Export spherical coordinates
coord_file_path = file_path + "/sphereCoordData.txt"

if Path(coord_file_path).is_file():
        with open(coord_file_path, 'a') as coord_file:
            coord_file.write(coord_data)
    else:
        with open(coord_file_path, 'w') as coord_file:
            coord_file.write(coord_data)
            
# User input values
antenna_frequency = float(input("Antenna Frequency: ")) # add frequency checking for SDR

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
        time.sleep(time_wait_2)
        
        ##### JOSH'S CODE #####
        data.saveSignal(antenna_frequency, file_path)

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