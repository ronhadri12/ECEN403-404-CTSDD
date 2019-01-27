
from dronekit import VehicleMode, LocationGlobal
import scipy.integrate as integrate
import math
#############################################################################################
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


    return LocationGlobal(lat3,long3,altitude)

#############################################################################################################################




list_1 = Next_Point(337.98,32.5,30.594405,-96.334708,10)

print list_1
