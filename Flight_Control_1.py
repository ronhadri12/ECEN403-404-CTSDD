# The following is used for controlling a Hexacopter using a
# Raspberry Pi 3 Model B (RP3) and a Pixhawk 2, using Dronekit(Mavlink)


print ("Start simulator (SITL)")
import dronekit_sitl
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

# Import Dronekit-Python
from dronekit import connect, VehicleMode, time
import math
##############################################################################
# Function that returns the next point to fly to
def Next_Point(distance, angle, lat1, long1):

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

	list = [lat2,long2]

	return list
#####################################################################################################################

antenna_frequency = float(input("Antenna Frequency: "))

antenna_length = float(input("Antenna length: "))

wavelength = ( 3 * (10 ** 8)) / antenna_frequency

far_field = (2 * (antenna_length ** 2)) / wavelength # Far field calculation for antenna


########################################################################################################
# Connect to the vehicle
print("Connecting to a vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)


	# Sets up a connection over the RP3 ttyS0 serial port
	#vehicle = connect('/dev/ttyS0',wait_ready = True, baud = 921600)	#Checks to see if the drone has booted, has GPS fix, and
																		#comleted pre-arm



while not vehicle.is_armable:
	print "Waiting for vehicle to initialize..."
	time.sleep(1)

vehicle.channels.overrides['5'] = 1900  #simulates manual mode being active

while not vehicle.channels['5'] >= 1400:
	print("Turn on manual mode.")
	time.sleep(1)

while not vehicle.channels['6'] <=1400:
	print("Turn off antenna location set.")
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



while vehicle.channels['5'] >= 1400:		#if manual mode is on and antenna location has not been set
	vehicle.mode = VehicleMode("STABILIZE")
	# A switch on the remote will be used to toggle drone being controlled
	# by the user or the Raspberry Pi

	if vehicle.channels['6'] >= 1400:
		lat_ant = vehicle.location.global_frame.lat	#sets antenna latitude
		long_ant = vehicle.location.global_frame.long	#sets antenna londitude
		alt_ant = vehicle.location.global_frame.alt	#sets antenna altitude
		heading = vehicle.heading					#sets compass heading of drone at antenna



while vehicle.channels['5'] < 1400:		#if Channel 5 is off

	if heading >= 120 and heading <=240:
		degree_left = heading - 120 			# heading for far left of pattern (facing the antenna)
		degree_right = heading + 120			# heading for far right of pattern (facing the antenna)
	elif heading < 120:							# vehicle.heading has a range of 0-360
		degree_left = 360 - (heading - 120)
		degree_right = heading + 120
	elif heading > 240:
		degree_left = heading - 120
		degree_right = 0 + (360 - heading)
	####################################################################################
	point_1 = Next_Point(far_field, degree_left, lat_ant, long_ant)

	vehicle.mode = VehicleMode("GUIDED")

	vehicle.simple_goto(point_1, 0.5)	# Commands the drone to go the the desired location at 0.5 m/s

	z = 0								# variable for incrementing
	point_list_arc1 = [0] * 60			# creates a list with 60 entries
	point_list_arc1[0] = point_1
	for i in range(148,88,-2):
		p1x_1 = far_field * math.sin(60)				#lines 139-145 are used to find the necessary distance to travel to next point on the first arc
		p1y_1 = far_field * math.cos(60)
		p2x_1 = far_field * math.sin(58)
		p2y_1 = far_field * math.cos(58)
		delta_x_1 = p2x_1 - p1x_1
		delta_y_1 = p2y_1 - p1y_1
		distance_change_1 = sqrt(delta_x_1 ** 2 + delta_y_1 ** 2)

		point_list_arc1[z+1] = Next_Point(distance_change_1, i, point_list_arc1[z[0]],point_list_arc1[z[1]])
		z = z + 1
	z = 0								# variable for incrementing
	point_list_arc2 = [0] * 60			# creates a list with 60 entries
	point_list_arc2[0] = point_60
	for i in range(90,152,2):
		p1x_2 = (far_field + 10) * math.sin(60)				#lines 139-145 are used to find the necessary distance to travel to next point on the second arc
		p1y_2 = (far_field + 10) * math.cos(60)
		p2x_2 = (far_field + 10) * math.sin(58)
		p2y_2 = (far_field + 10) * math.cos(58)
		delta_x_2 = p2x_2 - p1x_2
		delta_y_2 = p2y_2 - p1y_2
		distance_change_2 = sqrt(delta_x_2 ** 2 + delta_y_2 ** 2)

		point_list_arc2[z+1] = Next_Point(distance_change, i, point_list_arc2[z[0]],point_list_arc2[z[1]])
		z = z + 1

	z = 0								# variable for incrementing
	point_list_arc3 = [0] * 60			# creates a list with 60 entries
	point_list_arc3[0] = point_120
	for i in range(148,88,-2):
		p1x_3 = (far_field + 20) * math.sin(60)				#lines 139-145 are used to find the necessary distance to travel to next point on the third arc
		p1y_3 = (far_field + 20) * math.cos(60)
		p2x_3 = (far_field + 20) * math.sin(58)
		p2y_3 = (far_field + 20) * math.cos(58)
		delta_x_3 = p2x_3 - p1x_3
		delta_y_3 = p2y_3 - p1y_3
		distance_change_3 = sqrt(delta_x_3 ** 2 + delta_y_3 ** 2)

		point_list_arc3[z+1] = Next_Point(distance_change_3, i, point_list_arc3[z[0]],point_list_arc3[z[1]])
		z = z + 1


############################################################################################

vehicle.mode = VehicleMode("STABILIZE")		#returns control back to user, in case of malfunction or


# Close vehicle object before exiting the script
vehicle.close()

#Shut down the simulator
sitl.stop()
print("Completed")
