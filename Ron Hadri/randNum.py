import random
import numpy as np
import matplotlib.pyplot as plt
import math
from math import sin, cos, sqrt, atan2, radians
import os
import pdb

# finds the number of lines in a file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


# specify which data set to analyze as the current one
dataSet = 3

# antenna origin coordinates in [latitude, longitude, meters]
antenna = [30.594405, -96.334708, 10]

# set previous gain values
#with open("C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\magtest.txt") as gainFile:
#    with open("prevGain.txt", "w") as prevGainFile:
#        for line in gainFile:
#            prevGainFile.write(line)

# read the files and store the parameters into corresponding lists
print("\nReading the files now.")
fFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\freqtest.txt"
gFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\magtest.txt"
freqFile = open(fFile, "r")
gainFile = open(gFile, "r")

# collect all data
Freqs = freqFile.readlines()
Gains = gainFile.readlines()

# default to first data set if data set is zero or less
if dataSet < 2:
    listGainNums = Gains[0]
    listFreqNums = Freqs[0]
    listPrevGainNums = listGainNums

# default to latest data set if data set is greater than upper bound
elif dataSet > file_len(gFile):
    listGainNums = Gains[file_len(gFile) - 1]
    listFreqNums = Freqs[file_len(gFile) - 1]
    listPrevGainNums = Gains[file_len(gFile) - 2]

# specify which data set to focus on assuming the data set entered is within the boundaries
else:
    listGainNums = Gains[dataSet - 1]
    listFreqNums = Freqs[dataSet - 1]
    listPrevGainNums = Gains[dataSet - 2]

# get rid of square brackets
listFreqNums = listFreqNums.replace("[", "")
listFreqNums = listFreqNums.replace("]", "")
listGainNums = listGainNums.replace("[", "")
listGainNums = listGainNums.replace("]", "")
listPrevGainNums = listPrevGainNums.replace("[", "")
listPrevGainNums = listPrevGainNums.replace("]", "")

freqFile.close()
gainFile.close()

# split string into respective numbers
listFreqNums = listFreqNums.split(', ')
listGainNums = listGainNums.split(', ')
listPrevGainNums = listPrevGainNums.split(', ')

#######################################################################################################################
# write the files that would normally be received from Josh's subsystem
gpsFile = open("gps.txt", "w")

gpsCoord = [0, 0, 0]                            # list used to file corresponding XYZ coordinates of gpsNumsList
antOrigin = [10, 0, 20]                         # antenna origin relative to base station
gpsNumsList = []                                # list of lists of XYZ GPS coordinates relative to base station
gpsDiffNumsList = []                            # list of lists of XYZ GPS coordinates relative to antenna origin

# write the files with random parameters
for i in range(len(listFreqNums)):
    for j in range(3):
        gps = random.uniform(0, 40)
        gpsFile.write("%f\n" % gps)

gpsFile.close()

gpsFile = open("gps.txt", "r")
listGpsNums = gpsFile.read().splitlines()
gpsFile.close()
#######################################################################################################################

# type conversions
for i in range(len(listFreqNums)):
    listFreqNums[i] = float(listFreqNums[i])
    listGainNums[i] = float(listGainNums[i])
    listGainNums[i] = 10 * math.log10(listGainNums[i])
    listPrevGainNums[i] = float(listPrevGainNums[i])
    listPrevGainNums[i] = 10 * math.log10(listPrevGainNums[i])

for i in range(len(listGpsNums)):
    listGpsNums[i] = float(listGpsNums[i])

# make the GPS coordinates into a list of XYZ coordinate lists
for i in range(2, len(listGpsNums), 3):
    gpsCoord = [listGpsNums[i - 2], listGpsNums[i - 1], listGpsNums[i]]
    gpsNumsList.append(gpsCoord)

# do (antenna origin) - (GPS coordinates of measured values) to get GPS coordinates relative to antenna origin
for i in range(len(gpsNumsList)):
    gpsDiffNumsList.append(np.subtract(antOrigin, gpsNumsList[i]))

#######################################################################################################################
# Code snippet from online
R = 6373.0                      # approximate radius of earth in km

lat1 = radians(30.594202)
lon1 = radians(-96.325320)
lat2 = radians(30.595215)
lon2 = radians(-96.323542)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result:", distance)
#######################################################################################################################

# display the different lists
print('Frequency =', listFreqNums)
print('Gain =', listGainNums)
#print('GPS relative to base =', gpsNumsList)
print('GPS relative to antenna =', gpsDiffNumsList)

# calculate the parameters needed to plot the radiation pattern
theta = []
phi = []
r_array = []

for i in range(len(gpsDiffNumsList)):
    x = gpsDiffNumsList[i][0]
    y = gpsDiffNumsList[i][1]
    z = gpsDiffNumsList[i][2]
    r = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
    r_array.append(math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2)))
    phi.append(math.degrees(np.arccos(z / r)))
    theta.append(math.degrees(np.arctan(y / x)))

# display the parameters needed to plot the radiation pattern
#print('r =', r_array)
print('theta =', theta)
print('phi =', phi)

# create a file to store previous gain values
#prevGainFile = open("prevGain.txt")
#prevGainFile.close()

# copy over the current gain values if there are no previous gain values
#if os.stat("prevGain.txt").st_size == 0:
#    with open("gain.txt") as gainFile:
#        with open("prevGain.txt", "w") as prevGainFile:
#            for line in gainFile:
#                prevGainFile.write(line)

# percent error calculations
#else:
#    gainFile = open("gain.txt", "r")
#    prevGainFile = open("prevGain.txt", "r")
errorFile = open("error.txt", "w")
#    listPrevGainNums = prevGainFile.readline()                  # collect previous gain values from file
#    listPrevGainNums = listPrevGainNums.replace("[", "")
#    listPrevGainNums = listPrevGainNums.replace("]", "")
#    listPrevGainNums = listPrevGainNums.split(', ')#

print("Previous Gain =", listPrevGainNums)
errorList = []
for i in range(len(listGainNums)):                      # typecast previous gain values to floats
    errorNum = float(abs((listGainNums[i] - listPrevGainNums[i]) / listGainNums[i]))
    errorList.append(errorNum)

print(errorList)
errorFile.write(str(errorList))
errorFile.close()



# display error values
print("Error =", errorList)
errorFile.close()

avgError = (sum(errorList) / len(errorList)) * 100
print("Error between previous and current gain values = %f" % avgError, "%")

#######################################################################################################################
# test case to ensure that I can plot a radiation pattern correctly
thetaTest = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
             230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350]
gainTest = [0, -0.2, -1.2, -2.8, -4.2, -7, -9.5, -12, -15, -17.3, -21, -26, -32.4, -32.9, -32.9, -40, -39, -35, -33,
            -34.2, -38, -40, -39, -33.2, -28.9, -25.7, -22.9, -20.1, -16.5, -13.1, -10.2, -7.7, -4.6, -2.9, -1.5, -0.5]
for i in range(len(thetaTest)):
    thetaTest[i] = radians(thetaTest[i])

# plot test radiation pattern
plt.polar(thetaTest, gainTest)
plt.show()
#######################################################################################################################

# plot frequency vs. gain
plt.plot(listFreqNums, listGainNums, 'o')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Gain (dB)')
plt.title('Frequency (MHz) vs. Gain (dB)')
plt.show()

# create the other two files that will need to be sent to create the radiation pattern
thetaFile = open("theta.txt", "w")
phiFile = open("phi.txt", "w")
for i in range(len(theta)):
    thetaFile.write("%f\n" % theta[i])
    phiFile.write("%f\n" % phi[i])
thetaFile.close()
phiFile.close()
