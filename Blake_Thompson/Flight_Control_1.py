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
######################################################################################################
def Heading_to_unit_circle(heading_degree):         # Converts compass heading to comparable unit circle degree, since the Next_point function uses an input of unit circle degrees
                                                    # Compass heading increases with rotation in the clockwise direction
                                                    # Unit circle angle increases with rotation in counter-clockwise direction

    if 90 < heading_degree <= 360:                       # Checks to make sure that the input angle does not exceed 360 and instead starts back over at 0
        unit_circle_degree = (360 - heading_degree) + 90
    elif 0 <= heading_degree <= 90:
        unit_circle_degree = 90 - heading_degree

    return unit_circle_degree



#####################################################################################################################
# Function used to calculate GPS coordinates for drone to fly to

def GPS_Coords(far_field, heading, lat_ant, long_ant, alt_ant, number_points):
    if heading > 120 and heading <=240:
    	degree_left = heading - 120 			# heading for far left of pattern (starting facing the antenna)
    	degree_right = heading + 120			# heading for far right of pattern (starting facing the antenna)
    elif heading < 120:							# vehicle.heading has a range of 0-360
    	degree_left = 360 - (120 - heading)
    	degree_right = heading + 120
    elif heading > 240:
    	degree_left = heading - 120
    	degree_right = (heading + 120) - 360


    new_degree_left = Heading_to_unit_circle(degree_left)       # Converts left most degree of travel to unit circle angle
    new_degree_right = Heading_to_unit_circle(degree_right)     # Converts right most degree of travel to unit circle angle

    point_1 = Next_Point(far_field, new_degree_left, lat_ant, long_ant,alt_ant) # Calculates first point to fly to

    degree = 120 / (number_points - 1)            # Angle between each point, referenced from antenna (degrees)
    degree_polar = (degree  * math.pi)  / 180     # Angle between each point, referenced from antenna (polar)


    z = 0								            # Variable for incrementing in teh following for loop
    point_list_arc1 = [0] * number_points			# Creates a list with number of entries equal to the number of desired points for the drone to travel to
    point_list_arc1[0] = point_1                    # Fills the first GPS coordiate of the path into the list



    for i in range(new_degree_left + degree,new_degree_left + (120 + degree) ,degree):	# Calculates the next 11 points with 12 degrees of change between each, and fills all 60 points into a list
        if i >= 360:                    # Checks to make sure that the input angle does not exceed 360 and instead starts back over at 0
            next_angle = i - 360
        else:
            next_angle = i


        point_list_arc1[z+1] = Next_Point(far_field, next_angle, 30.594405, -96.334708,alt_ant)     # Fills in list with desired number of GPS coordinates
        z = z + 1

    return (point_list_arc1)     # Output list of GPS coordinates to terminal

########################################################################################################
# User input values
antenna_frequency = float(input("Antenna Frequency: "))

antenna_length = float(input("Antenna length: "))

wavelength = float(( 3 * (10 ** 8)) / antenna_frequency)

far_field = float((2 * (antenna_length ** 2)) / wavelength) # Far field calculation for antenna

number_points = input("Number of points (MUST be odd number): ")        # MUST be an odd number, to satisfy 'range' used in GPS_Coords function
while number_points < 2:
    print("Minimum number of 2 points required.")
    number_points =  ("Number of points: ")
while number_points % 2 == 0:
    print('Number of points must be odd.')
    number_points = ("Number of points: ")

########################################################################################################
# Connect to the vehicle, perform checks, and give control of drone to user
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
vehicle.flush()

print("Stabilize")

############################################################################################
# Manual Flight

while vehicle.channels['5'] >= 1200:		#if Flight Mode = 0 or 1 on controller, it is in manual flight

	# A switch on the remote will be used to toggle drone being controlled
	# by the user or the Raspberry Pi
    print("Manual flight")

    while vehicle.channels['5'] > 1600:		#if Flight Mode = 0 on controller, it is gathering antenna coordinates
	lat_ant = vehicle.location.global_frame.lat	#sets antenna latitude
	long_ant = vehicle.location.global_frame.lon	#sets antenna londitude
	alt_ant = vehicle.location.global_frame.alt	#sets antenna altitude
	heading = vehicle.heading					#sets compass heading of drone at antenna
        print("Gathering data")
        time.sleep(1)
    time.sleep(1)

if heading > 120 and heading <=240:
	degree_left = heading - 120 			# heading for far left of pattern (starting facing the antenna)
	degree_right = heading + 120			# heading for far right of pattern (starting facing the antenna)
elif heading < 120:							# vehicle.heading has a range of 0-360
	degree_left = 360 - (120 - heading)
	degree_right = heading + 120
elif heading > 240:
	degree_left = heading - 120
	degree_right = (heading + 120) - 360


new_degree_left = Heading_to_unit_circle(degree_left)       # Converts left most degree of travel from compass heading to unit circle angle
new_degree_right = Heading_to_unit_circle(degree_right)     # Converts right most degree of travel from compass heading to unit circle angle


GPS_Coord_List = GPS_Coords(far_field, heading, lat_ant, long_ant, alt_ant, number_points) # Uses GPS_Coords function to calculate all points to fly to

print("Got Coordinates")

velocity = float(0.5)							# Determines how fast the drone will fly
time_wait_1 = (far_field / velocity) + 0.5		# Calculates time (seconds) before next command is issued so drone can get to next location
point_1 = GPS_Coord_List[0]                     # Extractst the first point from the list of GPS coordinates
lat1 = point_1[0]                               # Extracts the latidude of the first coordinate
long1 = point_1[1]                              # Extracts the latidude of the first coordinate
alt1 = point_1[2]                               # Extracts the altitude of the first coordinate
################################################################################################
# Autonomous Flight

vehicle.mode = VehicleMode("GUIDED")
vehicle.flush()

while not vehicle.mode.name=='GUIDED':              # Checks to make sure vehicle is in GUIDED moded
    print("Vehicle not in GUIDED mode")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.flush()
    time.sleep(1)

while vehicle.channels['5'] < 1200:		# If Flight Mode = 2 on controller, it is in autonomous mode

    if vehicle.channels['5'] >=  1200:
        break

	vehicle.simple_goto(LocationGlobal(lat1, long1, alt1), velocity)	# Commands the drone to go the the desired location at 0.5 m/s
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
    print("Time_wait_2:", time_wait_2)
    print("Time_wait_1:", time_wait_1)



    for i in range(1,number_points,1):	# Iterates through and travels to specified number of points
        if vehicle.channels['5'] >=  1200:
            break
	current_point = GPS_Coord_List[i]         # Extracts next GPS Location to go to from GPS_Coord_List
	lat_loop = current_point[0]               # Extracts the latidude of the next coordinate
	long_loop = current_point[1]              # Extracts the latidude of the next coordinate
        alt_loop = current_point[2]               # Extracts the altitude of the next coordinate

	vehicle.simple_goto(LocationGlobal(lat_loop, long_loop, alt_loop),velocity)

        for t in range(1,int(math.ceil(time_wait_2)) * 2, 1):     # Continuously checks for operator overrride to return to manual control
            if vehicle.channels['5'] >=  1200:
                break
            time.sleep(0.5)



    for t in range(1,1000, 1):                      # Drone waits for operator to take control once it has completed the path
        if vehicle.channels['5'] >=  1200:
            break
        time.sleep(0.5)


############################################################################################
# Manual Control
vehicle.mode = VehicleMode("STABILIZE")
vehicle.flush		# Returns control back to user, in case of malfunction or end of flight path
