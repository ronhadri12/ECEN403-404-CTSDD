# The following is used for controlling a Hexacopter using a
# Raspberry Pi 3 Model B (RP3) and a Pixhawk 2.4.8, using Dronekit(Mavlink)




# Import Dronekit-Python
from dronekit import connect, VehicleMode, time
import math


##############################################################################
# Function that returns the next point to fly to
def Next_Point(distance, angle, lat1, long1,altitude):

    #Calculates length between each degree of longitude, based on latitude coordinate

	arc_length_per_degree = 111317.4306 #arc length per degree of earth's circumference (meters)

	long_difference = math.cos(lat1) * arc_length_per_degree	#dependent on latitude




	dx = distance * math.sin(angle)     # Change in x direction
	dy = distance * math.cos(angle)     # Change in y direction

	delta_longitude = dx / (111131.5 * math.cos(lat1)) # Converts change in x to change in longitude [degrees]

        # Distance between each degree of latitude varies between 110949 [m] and 111314 [m].
        # Average of the two used since distance differences of project is so small

	delta_latitude = dy / long_difference   # Converts change in y to change in latitude [degrees]

	long2 = long1 + delta_longitude         # Adds change in longitude to original longitude to give new longitude point
	lat2 = lat1 + delta_latitude            # Adds change in latitude to original latitude to give new latitude point

	list = [lat2,long2,altitude]

	return list
#####################################################################################################################
# User input values
antenna_frequency = float(input("Antenna Frequency: "))

antenna_length = float(input("Antenna length: "))

wavelength = float(( 3 * (10 ** 8)) / antenna_frequency)

far_field = float((2 * (antenna_length ** 2)) / wavelength) # Far field calculation for antenna


########################################################################################################
# Connect to the vehicle, perform checks, take off and hold at altitude
print("Connecting to a vehicle on: /dev/ttyS0")
vehicle = connect('/dev/ttyS0',wait_ready = True, baud = 921600)	#Checks to see if the drone has booted, has GPS fix, and
																		#comleted pre-arm



while not vehicle.is_armable:
	print "Waiting for vehicle to initialize..."
	time.sleep(1)



while not vehicle.channels['5'] >= 1200:
	print("Turn on manual mode: Flight Mode = 0")
	time.sleep(1)


vehicle.mode = VehicleMode("GUIDED")	#mode necessary to take off

print("Mode: %s") %vehicle.mode.name

while not vehicle.armed:				#waits for vehicle to be armed
	vehicle.armed = True
	time.sleep(1)
print("TEST")

print("Armed: %s") %vehicle.armed

print("Taking off")
vehicle.simple_takeoff(5)				#Takes off and flies up five meters and holds

time.sleep(3)

print("At height")

vehicle.mode = VehicleMode("STABILIZE")		#enables user control

print("Stabilize")

############################################################################################
# Manual flight

while vehicle.channels['5'] >= 1200:		#if Flight Mode = 0 or 1 on controller

	# A switch on the remote will be used to toggle drone being controlled
	# by the user or the Raspberry Pi

	while vehicle.channels['5'] > 1600:		#if Flight Mode = 0 on controller
		lat_ant = vehicle.location.global_frame.lat	#sets antenna latitude
		long_ant = vehicle.location.global_frame.long	#sets antenna londitude
		alt_ant = vehicle.location.global_frame.alt	#sets antenna altitude
		heading = vehicle.heading					#sets compass heading of drone at antenna

if heading >= 120 and heading <=240:
	degree_left = heading - 120 			# heading for far left of pattern (starting facing the antenna)
	degree_right = heading + 120			# heading for far right of pattern (starting facing the antenna)
elif heading < 120:							# vehicle.heading has a range of 0-360
	degree_left = 360 - (heading - 120)
	degree_right = heading + 120
elif heading > 240:
	degree_left = heading - 120
	degree_right = 0 + (360 - heading)

point_1 = Next_Point(far_field, degree_left, lat_ant, long_ant,alt_ant) #calculates first point
################################################################################################
# Autonomous Flight

vehicle.mode = VehicleMode("GUIDED")

while vehicle.channels['5'] < 1200:		#if Flight Mode = 2 on controller


	velocity = float(0.5)
	time_wait_1 = (far_field / velocity) + 2		#calculates time before next command is issued so drone can get to next location

	vehicle.simple_goto(point_1, velocity)	# Commands the drone to go the the desired location at 0.5 m/s
	time.sleep(time_wait_1)

	z = 0								# variable for incrementing
	point_list_arc1 = [0] * 60			# creates a list with 60 entries
	point_list_arc1[0] = point_1
	p1x_1 = far_field * math.sin(60)				#lines 128-136 are used to find the necessary distance to travel to next point on the first arc
	p1y_1 = far_field * math.cos(60)
	p2x_1 = far_field * math.sin(58)
	p2y_1 = far_field * math.cos(58)
	delta_x_1 = p2x_1 - p1x_1
	delta_y_1 = p2y_1 - p1y_1
	distance_change_1 = sqrt(delta_x_1 ** 2 + delta_y_1 ** 2)
	current_point = [0] * 2

	if degree_left >= 90:
		arc_degree_left = degree_left - 90
	elif degree_left < 90:
		arc_degree_left = 360 - (90 - degree_left)			#lines 138-145 are used to find the starting and ending angle (heading) that the drone will travel to
	if degree_right <= 270:
		arc_degree_right = degree_right + 90
	elif degree_right > 270:
		arc_degree_right = 90 - (360 - degree_right)


	for i in range(arc_degree_left,arc_degree_right,-2):	#iterates through and travels to 60 points with 2 degrees of change between them

		current_point = point_list_arc1[z]
		lat = current_point[0]
		long = current_point[1]
		point_list_arc1[z+1] = Next_Point(distance_change_1, i, lat,long, alt_ant)
		z = z + 1

		time_wait_2 = (distance_change_1 / velocity) + 0.5
		vehicle.simple_goto(point_list_arc1[z],velocity)

		time.sleep(time_wait_2)					#calculates time before next command is issued so drone can get to next location


	time.sleep(1000)



############################################################################################

vehicle.mode = VehicleMode("STABILIZE")		#returns control back to user, in case of malfunction or end of flight path
