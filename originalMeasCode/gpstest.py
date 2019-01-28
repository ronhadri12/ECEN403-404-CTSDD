# This is the original file/code for gpsdata.py
from dronekit import connect
from pathlib2 import Path

print("Connecting to a vehicle on: /dev/ttyS0")
vehicle = connect("/dev/ttyS0", wait_ready = True, baud = 921600)

gps_file_path = '/home/pi/gpstest.txt'

# extract data
lat_data = vehicle.location.global_frame.lat
lon_data = vehicle.location.global_frame.lon
alt_data = vehicle.location.global_frame.alt

# write data
if Path(gps_file_path).is_file():
    with open(gps_file_path, 'a') as gps_file:
        gps_file.write('[%s, %s, %s], ' % (lat_data, lon_data, alt_data))
else:
    with open(gps_file_path, 'w') as gps_file:
        gps_file.write('[%s, %s, %s], ' % (lat_data, lon_data, alt_data))


# verification
print("Latitude: %s" % lat_data)
print("Longitude: %s" % lon_data)
print("Altitude: %s" % alt_data)


