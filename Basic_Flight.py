

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

wavelength = ( 3 * (10 ** 8)) / antenna_frequency

far_field = (2 * (antenna_length ** 2)) / wavelength # Far field calculation for antenna


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

	if vehicle.channels['5'] > 1600:		#if Flight Mode = 0 on controller
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

vehicle.mode = VehicleMode("GUIDED")

################################################################################################
# Autonomous Flight
while vehicle.channels['5'] < 1200:		#if Flight Mode = 2 on controller



	vehicle.simple_goto(point_1, 0.5)	# Commands the drone to go the the desired location at 0.5 m/s
	time.sleep(1000)
vehicle.mode = VehicleMode("STABILIZE")
