
import math

heading = 322
far_field = 6.5                             # distance of points from antenna in the far field
number_points = 11                          # number of points per path
height  = [0]                    # number of vertiacl meters BELOW the antenna
number_paths = 1                            # Number of paths to be run
#gain = [-20, -17,-16,-15,-14,-13,-14,-15,-16,-17,-20,-10,-7,-6,-5,-4,-3,-4,-5,-6,-7,-10,-7,-4,-3,-2,-1,0,-1,-2,-3,-4,-7,-17,-14,-13,-12,-11,-10,-11,-12,-13,-14,-17]
degree = 120 / (number_points - 1)            # Angle between each point, referenced from antenna (degrees)

def Rons_Stuff(far_field,number_points,height,number_paths,degree):

    degree_polar = (degree  * math.pi)  / 180

    theta = [0] * number_paths                       # Creates list for theta angle for each path number
    phi = [0] * number_points                       # Creates list for phi angle for each point on horizontal path

    for i in range(0,number_paths,1):           # finds theta angle a distance down from the antenna
        theta_polar = math.atan(float(height[i]) / float(far_field))
        theta[i] = ((theta_polar / math.pi) * 180)

    normal_vector_point_number = number_points / 2

    for i in range(0,number_points,1):
        if i < normal_vector_point_number:
            points_from_normal = normal_vector_point_number - i     # points_from_normal is the number of points from the point that lies on the normal vector            phi[i] = degree * points_from_normal                  # determines phi for the points that are to the left of the path
            phi[i] = degree * points_from_normal
        elif i == normal_vector_point_number:
            phi[i] = 0                                            # determines phi for the point that lies on the normal vector
        elif i > normal_vector_point_number:
            points_from_normal = i - normal_vector_point_number
            phi[i] = degree * points_from_normal                  # determines phi for the points that are to the right of the path

    total_number_points = number_points * number_paths          # calculates total number of points to fly to

    output = [0] * (total_number_points)                             # list that holds the info for each point

    #output = []
    point_info_vector = [0] * 3                                 # list to hold the distance, theta, phi, and gain for each points

    for i in range(1,total_number_points+1,1):
        point_info_vector=[0,0,0]                             # resets the point_info_vector to be filled in for loop

        point_info_vector[1] = (theta[ (i-1) / number_points ]) + 90   # second entry is the theta angle(angle from normal vector on horizontal plane)

        if ((i-1) / number_points) % 2 == 0:
            point_info_vector[2] = phi[ ((i-1) % number_points) ]       # third entry is the phi angle (angle from vertical axis)
        else:
            point_info_vector[2] = phi[ (10 - ((i-1) % 11)) ]

        final_degree = ((point_info_vector[1] - 90) * math.pi) / 180       #converts theta angle to radians

        point_info_vector[0] = far_field / math.cos(final_degree)   # first entry is the distance from antenna



        output[i-1] = point_info_vector                         # puts the point_info_vector into

    return(output)
    #print(i)
    #print(output[i-1])

out = Rons_Stuff(far_field,number_points,height,number_paths,degree)
print(out)
