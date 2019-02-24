import measurements as data
import Ron_Stuff as ron
from pathlib2 import Path

# Find directory for exporting data
file_path = data.filePath()

# Calculate spherical coordinates
far_field = 6.5                              # distance of points from antenna in the far field
number_points = 11                          # number of points per path
height = [0]                    # number of vertiacl meters BELOW the antenna
number_paths = 1                            # Number of paths to be run
gain = [-20, -17,-16,-15,-14,-13,-14,-15,-16,-17,-20,-10,-7,-6,-5,-4,-3,-4,-5,-6,-7,-10,-7,-4,-3,-2,-1,0,-1,-2,-3,-4,-7,-17,-14,-13,-12,-11,-10,-11,-12,-13,-14,-17]
degree = 120 / (number_points - 1)

coord_data = ron.Rons_Stuff(far_field, number_points, height, number_paths, degree)

# Export spherical coordinates
coord_file_path = file_path + "/sphereCoordData.txt"

if Path(coord_file_path).is_file():
    with open(coord_file_path, 'a') as coord_file:
        for item in coord_data:
            coord_file.write("%s\n" % item)
else:
    with open(coord_file_path, 'w') as coord_file:
        for item in coord_data:
            coord_file.write("%s\n" % item)
            
# Confirmation
print("Spherical coordinates saved to: %s" % coord_file_path)

# Collect signal data
freq = 95100000.0

# data.saveSignal(freq, file_path)
