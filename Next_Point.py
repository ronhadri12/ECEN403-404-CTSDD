# Script to determine next coordinate(lat, long), based on current
# location, desired angle, desired distance

import math


def Next_Point(distance, angle, lat1, long1):
    #distance = float(input("Distance from current location (meters): "))
    distance = 10
    #angle = float(input("Angle from current location (degrees): "))
    angle = 293

    #lat1 = float(input("Current latitude: "))
    #long1 = float(input("Current longitude: "))
    lat1 = 32.776664
    long1 = -96.7969879

    ################################################################

    #Calculates length between each degree of longitude, based on latitude coordinate

    arc_length_per_degree = 111317.4306 #arc length per degree of earth's circumference (meters)

    long_difference = math.cos(lat1) * arc_length_per_degree


    ################################################################

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




point_1 = Next_Point(10,293,32.776664,-96.7969879)

print(point_1[0])
print(point_1[1])
