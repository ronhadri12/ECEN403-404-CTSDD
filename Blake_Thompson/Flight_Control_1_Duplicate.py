# The following is used for controlling a Hexacopter using a
# Raspberry Pi 3 Model B (RP3) and a Pixhawk 2.4.8, using Dronekit(Mavlink)




# Import Dronekit-Python
from dronekit import connect, VehicleMode, time, LocationGlobal
import math
import scipy.integrate as integrate


##############################################################################
# Function that returns the next point to fly to
def Next_Point(distance, angle, lat1, long1, altitude):

    lat2 = (lat1 * math.pi) / 180               # Converts latitude angle to radians
    long2 = (long1 * math.pi) / 180             # Converts longitude angle to radians


    lower_lat = math.floor(lat1)     # Finds the latitude line above the current location
    upper_lat = math.ceil(lat1)      # Finds the latitude line below the current location

    polar_lower_lat = (lower_lat * math.pi) / 180   # Converts lower_lat to radians since trig functions in 'math' use radians
    polar_upper_lat = (upper_lat * math.pi) / 180   # Converts upper_lat to radians since trig functions in 'math' use radians

    lower_angle = (math.atan((6378137.0/6356752.0) * math.tan(polar_lower_lat)))    # Angle (polar) between equator and upper latitude line
    upper_angle = (math.atan((6378137.0/6356752.0) * math.tan(polar_upper_lat)))    # Angle (polar) between equator and upper latitude line
                                                                                    # 6356752.0 = Polar radius of Earth      (meters)
                                                                                    # 6378137.0 = Equitorial radius of Earth (meters)


    def integrand(x):
        return math.sqrt(((6378137**2) * ((math.sin(x))**2)) + ((6356752**2) * ((math.cos(x))**2)))

    lat_difference1 = integrate.quad(integrand, lower_angle, upper_angle)           # Integral to find the arc length between latitiude lines of the earth (meters)

    lat_difference2 = lat_difference1[0]    # integrate.quad outputs  a tuple with two items in the list, this extracts the first and leaves the error

    angle_rad = (angle * math.pi) / 180     # Direction that drone will be traveling, given in terms of the unit circle (radians)

    arc_length_per_degree = 111317.4306     # Arc length per degree of longitude at Earth's equator (meters)

    long_difference = math.cos(lat2) * arc_length_per_degree  # Calculates length between each degree of longitude, based on latitude coordinate


    dx = distance * math.cos(angle_rad)     # Change in x direction (meters)
    dy = distance * math.sin(angle_rad)     # Change in y direction (meters)

    delta_longitude = dx / long_difference  # Converts change in x to change in longitude   (meters)

    delta_latitude = dy / lat_difference2   # Converts change in y to change in latitude    (meters)


    long3 = long1 + delta_longitude         # Adds change in longitude to original longitude to give new longitude point
    lat3 = lat1 + delta_latitude            # Adds change in latitude to original latitude to give new latitude point


    return [lat3,long3,altitude]


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


print("Armed: %s") %vehicle.armed
time.sleep(2)

print("Taking off")
vehicle.simple_takeoff(3)				#Takes off and flies up five meters and holds

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

point_1 = Next_Point(far_field, degree_left, lat_ant, long_ant,alt_ant) #calculates first point to fly to from antenna

################################################################################################
# Autonomous Flight

vehicle.mode = VehicleMode("GUIDED")

while vehicle.channels['5'] < 1200:		#if Flight Mode = 2 on controller


	velocity = float(0.5)							#Determines how fast the drone will fly
	time_wait_1 = (far_field / velocity) + 2		#calculates time before next command is issued so drone can get to next location

	vehicle.simple_goto(LocationGlobal(point_1[0], point_1[1], point_1[2]), velocity)	# Commands the drone to go the the desired location at 0.5 m/s
	time.sleep(time_wait_1)

	z = 0								# variable for incrementing
	point_list_arc1 = [0] * 60			# creates a list with 60 entries
	point_list_arc1[0] = point_1
	p1x_1 = far_field * math.sin(60)	#lines 136-142 are used to find the necessary distance to travel to next point on the first arc
	p1y_1 = far_field * math.cos(60)
	p2x_1 = far_field * math.sin(58)
	p2y_1 = far_field * math.cos(58)
	delta_x_1 = p2x_1 - p1x_1
	delta_y_1 = p2y_1 - p1y_1
	distance_change_1 = sqrt(delta_x_1 ** 2 + delta_y_1 ** 2)		#distance change between two points
	current_point = [0] * 2

	if degree_left >= 90:
		arc_degree_left = degree_left - 90
	elif degree_left < 90:
		arc_degree_left = 360 - (90 - degree_left)			#lines 166-173 are used to find the starting and ending angle (heading) that the drone will travel to
	if degree_right <= 270:
		arc_degree_right = degree_right + 90
	elif degree_right > 270:
		arc_degree_right = 90 - (360 - degree_right)


	for i in range(arc_degree_left,arc_degree_right,-2):	#iterates through and travels to 60 points with 2 degrees of change between them (total of 120 degrees)

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
