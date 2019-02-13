import measurements as data
import os

while True:
    storage = input("Where do you want to export the data?"
                    "\n[1] Onboard storage \n[2] External drive \n")
    # Onboard storage
    if storage == 1:
        file_path = "/home/pi"
    # External drive
    elif storage == 2:
        drive_name = raw_input("Please enter the name of the external drive: ")
        file_path = "/media/pi/" + drive_name
        # Check for specified external drive
        while os.path.exists(file_path) != True:     
            drive_name = raw_input("The file path %s not exist. Export data "
                                   "to onboard storage? [Y/N] " % file_path)
            if drive_name == "Y" or drive_name == "y":
                file_path = "/home/pi"
                break
            elif drive_name == "N" or drive_name == "n":
                drive_name = raw_input("Please enter the name of the external drive: ")
                file_path = "/media/pi/" + drive_name
            else:
                print("Please enter [Y] or [N].")
    else:
        print("Please enter [1] or [2].\n")
    
    # Confirm save location    
    confirm = raw_input("Data will be exported to: %s [Y/N] " % file_path)
    
    if confirm == "Y" or confirm == "y":
        break
    elif confirm == "N" or confirm == "n":
        continue
    else:
        print("Error: Inavlid input")

# Confirmation
print("Exporting data to: %s" % file_path)

freq = 95100000.0

data.saveSignal(freq, file_path)
