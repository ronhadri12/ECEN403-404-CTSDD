points_per_path = input("Points per path: ")
number_paths = input("Number of paths: ")
total_points = points_per_path * number_paths
alt_ant = 50

alt_list = [0] * number_paths
for i in range(0,len(alt_list),1):               # Drops each consecutive flight path by 1 meter
    alt_list[i] = alt_ant - (i * 1)


import math
import scipy.integrate as integrate

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
    print("dy: ", dy)

    long3 = long1 + delta_longitude         # Adds change in longitude to original longitude to give new longitude point
    lat3 = lat1 + delta_latitude            # Adds change in latitude to original latitude to give new latitude point


    return [lat3,long3,altitude]
######################################################################################################
# Converts compass heading to comparable unit circle degree, since the Next_point function uses an input of unit circle degrees
def Heading_to_unit_circle(heading_degree):
                                                    # Compass heading increases with rotation in the clockwise direction
                                                    # Unit circle angle increases with rotation in counter-clockwise direction

    if 90 < heading_degree <= 360:                       # Checks to make sure that the input angle does not exceed 360 and instead starts back over at 0
        unit_circle_degree = (360 - heading_degree) + 90
    elif 0 <= heading_degree <= 90:
        unit_circle_degree = 90 - heading_degree

    return unit_circle_degree



#####################################################################################################################
# Function used to calculate GPS coordinates for drone to fly to

def GPS_Coords(far_field, heading, lat_ant, long_ant, alt_ant, points_per_path, number_paths):
    total_points = points_per_path * number_paths


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

    #point_1 = Next_Point(far_field, new_degree_left, lat_ant, long_ant,alt_ant[0]) # Calculates first point to fly to

    degree = 120 / (points_per_path - 1)            # Angle between each point, referenced from antenna (degrees)
    degree_polar = (degree  * math.pi)  / 180     # Angle between each point, referenced from antenna (polar)


    z = 0								            # Variable for incrementing in teh following for loop
    point_list_arc1 = [0] * total_points			# Creates a list with number of entries equal to the number of desired points for the drone to travel to
    #point_list_arc1[0] = point_1                    # Fills the first GPS coordiate of the path into the list
    print(new_degree_left)
    print(new_degree_right)

    for z in range(0,total_points,1):                               # A for loop that goes through each point to assign a GPS location to it
        if ((z/points_per_path) % 2) == 0:                          # Checks for even number paths (path starts on left)
            i = ((z % points_per_path) * degree) + new_degree_left
            if i >= 360:                                            # Ensures that angle wraps back around if angle is greater than 360
                next_angle = i - 360
            else:
                next_angle = i

            print(next_angle)
            point_list_arc1[z] = Next_Point(far_field, next_angle, lat_ant, long_ant,alt_list[z / points_per_path])     # Fills in list with desired number of GPS coordinates


        if ((z/points_per_path) % 2) == 1:                          # Checks for even number paths (path starts on right)
            i = new_degree_right - ((z % points_per_path) * degree)
            if i < 0:                                               # Ensures that angle wraps back around if angle is less than 0
                next_angle = (360 + i)
            else:
                next_angle = i
            print(next_angle)


            point_list_arc1[z] = Next_Point(far_field, next_angle, lat_ant, long_ant,alt_list[z / points_per_path])     # Fills in list with desired number of GPS coordinates



    return (point_list_arc1)     # Output list of GPS coordinates to terminal


print(GPS_Coords(10, 20, 30.594254, -96.334678, alt_list, points_per_path, number_paths))
