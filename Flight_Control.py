# The following is used for controlling a Hexacopter using a 
# Raspberry Pi 3 Model B (RP3) and a Pixhawk 2, using Dronekit(Mavlink)


from dronekit import connect  

# Program that calculates the points for the drone to fly to 
from Location_Calculation import Locations

	# Sets up a connection over the RP3 ttyS0 serial port
	vehicle = connect('/dev/ttyS0',wait_ready = True, baud = 921600)

	#Checks to see if the drone has booted, has GPS fix, and 
	#comleted pre-arm
	while not vehicle.is_armable:
		print "Waiting for vehicle to initialize..."
		time.sleep(1)
		
	# A switch on the remote will be used to toggle drone being controlled 
	# by the user or the Raspberry Pi
	if (Insert RC channel controlled by remote) = 1
		vehicle.mode = VehicleMode("Guided")
		vehicle.armed = True
		
		# Sets the desired location for the drone
		# Pulled from Location_Calculation file
		point_1 = LoationGlobal(latitude, longitude, height(m/s)) 
	
		# Commands the drone to go the the desired location at 0.5 m/s
		vehicle.simple_goto(point_1, 0.5)
		
		# Add code to pull GPS location from Pixhawk and send to RP3

		# Add code to verify location using external GPS and Pixhawk GPS
		
		
		
		
	if (Insert RC channel controlled by remote) = 0
		vehicle.mode = VehicleMode("Acro")
	
	

	
