import os, sys

path = "/media/pi/"
dirs = os.listdir(path)





if dirs:
    usbpath = dirs[0]
    newpath = path + usbpath
else:
    newpath = path + "test"
    
print(newpath)
for file in dirs:
    print(file)
