def Heading_to_unit_circle(heading_degree):         # Converts compass heading to comparable unit circle deg
                                                    # Compass heading increases with rotation in the clockwise direction
                                                    # Unit circle degrees increase with rotation in counter-clockwise direction
    if 90 < heading_degree <= 360:
        unit_circle_degree = (360 - heading_degree) + 90
    elif 0 <= heading_degree <= 90:
        unit_circle_degree = 90 - heading_degree

    return unit_circle_degree
