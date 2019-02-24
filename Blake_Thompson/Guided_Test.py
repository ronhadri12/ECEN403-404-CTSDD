from dronekit import connect, VehicleMode, time, LocationGlobal
import math
import scipy.integrate as integrate


print("Connecting to a vehicle on: /dev/ttyS0")
vehicle = connect('/dev/ttyS0',wait_ready = True, baud = 921600)	#Checks to see if the drone has booted, has GPS fix, and
																		#comleted pre-arm



while not vehicle.is_armable:
	print "Waiting for vehicle to initialize..."
	time.sleep(1)


while not vehicle.channels['5'] >= 1200:
	print("Turn on manual mode(Flight Mode Switch = 1): Current Flight Mode Switch = 0")
	time.sleep(1)

# Flight Mode Switch position 2 = Guided Mode
# Flight Mode Switch position 1 = Manual Mode
# Flight Mode Switch position 0 = Manual Mode and capture GPS location of antenna

print("Mode: %s") %vehicle.mode.name

while not vehicle.armed:				#waits for vehicle to be armed
	vehicle.armed = True
	time.sleep(1)


print("Armed: %s") %vehicle.armed
time.sleep(2)



vehicle.mode = VehicleMode("STABILIZE")		#enables user control
vehicle.flush()



while vehicle.channels['5'] >= 1200:		#if Flight Mode = 0 or 1 on controller, it is in manual flight
    print("Should be in STABILIZE mode.")
    print(vehicle.mode.name)

    while vehicle.channels['5'] >=1600:
        print("Vehicle gathering data")

vehicle.mode = VehicleMode("GUIDED")
vehicle.flush()



while vehicle.channels['5'] < 1200
    while not vehicle.mode.name=='GUIDED':              # Checks to make sure vehicle is in GUIDED moded
        if vehicle.channels['5'] >=  1200:
            break
        print("Vehicle not in GUIDED mode")
        vehicle.mode = VehicleMode("GUIDED")
    if vehicle.channels['5'] >=  1200:
        break
    print("Should be in GUIDED mode")
    print(vehicle.mode.name)

vehicle.mode = VehicleMode("STABILIZE")
