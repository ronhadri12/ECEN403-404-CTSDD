# Script used to calculate GPS coordinates to fly to, based on number of points on path,

from dronekit import VehicleMode, LocationGlobal
import scipy.integrate as integrate
import math



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

#######################################################################################################


far_field = 17                              # Simulated far field distance of an antenna
heading = 280                               # Compass heading that the drone is facing, provided by vehicle.heading
lat_ant = 30.594405
long_ant = -96.334708
alt_ant = 2                                 # Altitude of antenna
number_points = 61                          # Number of points must be an odd in order to satsify the type requirement for 'range' on line 105
                                            # Even numbers cause degree to become a float, and 'range' cannot use float

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



print (point_list_arc1)     # Output list of GPS coordinates to terminal
