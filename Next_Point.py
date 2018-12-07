distance = 10
angle = 69
lat_1 = 32.97979798
long_1 = -97.5454545445
altitude = 10

from dronekit import VehicleMode, LocationGlobal
import math
#############################################################################################
def Next_Point(distance, angle, lat1, long1, altitude):

    lat2 = (lat1 * math.pi) / 180               #converts latitude angle to radians
    long2 = (long1 * math.pi) / 180             #converts longitude angle to radians


    angle_rad = (angle * math.pi) / 180   #heading in radians

    arc_length_per_degree = 111317.4306 #arc length per degree of earth's circumference (meters)

    long_difference = math.cos(lat2) * arc_length_per_degree  #Calculates length between each degree of longitude, based on latitude coordinate

    ################################################################

    dx = distance * math.cos(angle_rad)     # Change in x direction
    dy = distance * math.sin(angle_rad)     # Change in y direction

    delta_longitude = dx / long_difference      # Converts change in x to change in longitude

    delta_latitude = dy / 110863   # Converts change in y to change in latitude
                                    # 110863 is the distance between latitude line at 30.594114.
                                    # Constant because the variation in distance between latitude lines is so small
                                    # it can be kept constant

    long3 = long1 + delta_longitude         # Adds change in longitude to original longitude to give new longitude point
    lat3 = lat1 + delta_latitude            # Adds change in latitude to original latitude to give new latitude point


    return LocationGlobal(lat3,long3,altitude)





list_1 = Next_Point(336.61,33.2,30.594114,-96.3347661,10)

print list_1
