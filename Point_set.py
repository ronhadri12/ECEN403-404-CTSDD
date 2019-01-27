from dronekit import VehicleMode, LocationGlobal
import scipy.integrate as integrate
import math



def Next_Point(distance, angle, lat1, long1, altitude):

    lat2 = (lat1 * math.pi) / 180               #converts latitude angle to radians
    long2 = (long1 * math.pi) / 180             #converts longitude angle to radians


    lower_lat = math.floor(lat1)     #finds the latitude line above the current location
    upper_lat = math.ceil(lat1)      #finds the latitude line below the current location

    polar_lower_lat = (lower_lat * math.pi) / 180
    polar_upper_lat = (upper_lat * math.pi) / 180

    lower_angle = (math.atan((6378137.0/6356752.0) * math.tan(polar_lower_lat)))    #angle (polar) between equator and upper latitude line
    upper_angle = (math.atan((6378137.0/6356752.0) * math.tan(polar_upper_lat)))    #angle (polar) between equator and upper latitude line


    def integrand(x):
        return math.sqrt(((6378137**2) * ((math.sin(x))**2)) + ((6356752**2) * ((math.cos(x))**2)))

    lat_difference1 = integrate.quad(integrand, lower_angle, upper_angle)        # Integral to find the arc length between latitiude lines of the earth

    lat_difference2 = lat_difference1[0]       #integrate.quad outputs  a tuple with two items in the list, this pulls the first and leaves the error

    angle_rad = (angle * math.pi) / 180   #heading in radians

    arc_length_per_degree = 111317.4306 #arc length per degree of longitude at Earth's equator (meters)

    long_difference = math.cos(lat2) * arc_length_per_degree  #Calculates length between each degree of longitude, based on latitude coordinate


    dx = distance * math.cos(angle_rad)     # Change in x direction
    dy = distance * math.sin(angle_rad)     # Change in y direction

    delta_longitude = dx / long_difference      # Converts change in x to change in longitude

    delta_latitude = dy / lat_difference2   # Converts change in y to change in latitude
                                    # 111220 is the distance between latitude lines 30 and 31.
                                    # Constant because the variation in distance between latitude lines is so small
                                    # it can be kept constant(110574 m - 111694 m)

    long3 = long1 + delta_longitude         # Adds change in longitude to original longitude to give new longitude point
    lat3 = lat1 + delta_latitude            # Adds change in latitude to original latitude to give new latitude point


    return [lat3,long3,altitude]
######################################################################################################

far_field = 10
heading = 280
lat_ant = 30.594405
long_ant = -96.334708
alt_ant = 10


if heading >= 120 and heading <=240:
	degree_left = heading - 120 			# heading for far left of pattern (starting facing the antenna)
	degree_right = heading + 120			# heading for far right of pattern (starting facing the antenna)
elif heading < 120:							# vehicle.heading has a range of 0-360
	degree_left = 360 - (120 - heading)
	degree_right = heading + 120
elif heading > 240:
	degree_left = heading - 120
	degree_right = (heading + 120) - 360

point_1 = Next_Point(far_field, degree_left, lat_ant, long_ant,alt_ant) #calculates first point to fly to




z = 0								# Variable for incrementing in teh following for loop
point_list_arc1 = [0] * 60			# Creates a list with 60 entries to store the GPS Coordinates
point_list_arc1[0] = point_1        # Fills the first GPS coordiate of the path into the list
p1x_1 = far_field * math.sin(60)	#lines 79-85 are used to find the necessary distance to travel to next point on the first arc, assuming 2 degree separation between each point
p1y_1 = far_field * math.cos(60)
p2x_1 = far_field * math.sin(58)
p2y_1 = far_field * math.cos(58)
delta_x_1 = p2x_1 - p1x_1
delta_y_1 = p2y_1 - p1y_1
distance_change_1 = math.sqrt(delta_x_1 ** 2 + delta_y_1 ** 2)
current_point = [0] * 2             #

if degree_left >= 90:
    arc_degree_left = degree_left - 90
elif degree_left < 90:
    arc_degree_left = 360 - (90 - degree_left)			#lines 88-95 are used to find the starting and ending angle (heading) that the drone will travel to
if degree_right <= 270:
    arc_degree_right = 360 + (degree_right - 90)
elif degree_right > 270:
    arc_degree_right = 90 - (360 - degree_right)

    #arc_degree_left is the heading from the first calculated point to the second point, which is tangent to the heading used to get to the left-most point (degree_left)
    #arc_degree_left is the heading that the drone will be facing at the end of the path, which is tangent to the heading of the right most point (degree_left)



for i in range(2,120,2):	# Calculates the next 59 points with 2 degrees of change between each, and fills all 60 points into a list

    current_point = point_list_arc1[z]
    lat = current_point[0]
    lon = current_point[1]

    print(z)
    point_list_arc1[z+1] = Next_Point(distance_change_1, i, lat,lon, alt_ant)
    z = z + 1


print (point_list_arc1)
