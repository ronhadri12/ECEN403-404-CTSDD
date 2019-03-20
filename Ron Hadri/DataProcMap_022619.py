import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import math
from math import sin, cos, sqrt, atan2, radians, exp
import pdb
from scipy.interpolate import splprep, splev


#######################################################################################################################
# NOTE FOR FUTURE:
# Do error percent on gain and freq values of the same list, not different lists
#######################################################################################################################


# ___________________________________________________FUNCTIONS________________________________________________________ #
def file_len(fname):                                                        # finds the number of lines in a file
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def unique(list1):                                                          # get unique values in a list
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)

    return unique_list


# ___________________________________________________VARIABLES________________________________________________________ #
# lists used to store radiation pattern parameters
listDistNums = []
listThetaNums = []
listPhiNums = []
dist = []
theta = []
phi = []
gain = []
freq = []               # list used to store all frequency values

# lists used to store percent error calculations
errorList = []
avgError = []

# filtered lists used to plot
filtFreq = []
filtGain = []
filtDist = []
filtTheta = []
filtPhi = []

# store maximum gain values in radiation pattern
maxGainH = []
maxGainV = []
tempGainH = []
tempGainV = []

# store gain values to compare to frequency
filtGainFreq = []

posAngle = False        # determine whether horizontal angle is pos or neg depending on normal vector of antenna
freqRange = 0.005       # acceptable maximum and minimum frequency range from median value of frequencies
interpPoint = 0         # interpolated point at a certain angle

userLocation = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\";

# ______________________________________________________I/O___________________________________________________________ #
# read the files and store the parameters into corresponding lists
print("\nReading the files now.")
fFile = userLocation + "freqdata_022619.txt"
gFile = userLocation + "magdata_022619.txt"
gpsFile = userLocation + "coorddata_022619.txt"
freqFile = open(fFile, "r")
gainFile = open(gFile, "r")
dtpFile = open(gpsFile, "r")
errorFile = open("error.txt", "w")

# _____________________________________________________PARSE__________________________________________________________ #
# collect gain and frequency
Freqs = freqFile.readlines()
Gains = gainFile.readlines()
DTP = dtpFile.readlines()

for i in range(file_len(gFile)):
    listGainNums = Gains[i]
    listFreqNums = Freqs[i]
    DisThetaPhi = DTP[i]

    # get rid of square brackets
    listFreqNums = listFreqNums.replace("[", "")
    listFreqNums = listFreqNums.replace("]", "")
    listGainNums = listGainNums.replace("[", "")
    listGainNums = listGainNums.replace("]", "")
    DisThetaPhi = DisThetaPhi.replace("[", "")
    DisThetaPhi = DisThetaPhi.replace("]", "")

    # split string into respective numbers
    listFreqNums = listFreqNums.split(', ')
    listGainNums = listGainNums.split(', ')
    DisThetaPhi = DisThetaPhi.split(', ')

    # ________________________________________________ORGANIZE LISTS__________________________________________________ #
    # type conversions
    for j in range(len(DisThetaPhi)):
        DisThetaPhi[j] = float(DisThetaPhi[j])

    if ~posAngle:
        # sign of horizontal angle toggles after each time drone crosses the normal vector of the antenna
        if DisThetaPhi[2] == 0:
            posAngle = ~posAngle
        else:
            DisThetaPhi[2] = 360 - DisThetaPhi[2]

    for j in range(len(listFreqNums)):
        listFreqNums[j] = float(listFreqNums[j])
        listGainNums[j] = float(listGainNums[j])
        listGainNums[j] = float(10 * math.log10(listGainNums[j]))

        # lists of 11,264 elements
        gain.append(listGainNums[j])
        freq.append(listFreqNums[j])
        dist.append(DisThetaPhi[0])
        theta.append(DisThetaPhi[1])
        phi.append(DisThetaPhi[2])

        # ________________________________________PERCENT ERROR CALCULATIONS__________________________________________ #
        if j > 0:
            errorNum = float(abs((listGainNums[j] - listGainNums[j - 1]) / listGainNums[j]))
            errorList.append(errorNum)
            if j == (len(listFreqNums) - 1):
                avgError.append((sum(errorList) / len(errorList)) * 100)

totalAvgError = sum(avgError) / len(avgError)

# ______________________________________DISPLAY OUTPUT PARAMETERS_________________________________________ #
print("Average error between gain measurements for each point =", avgError)
print("Total average error of all measurements =", totalAvgError)
for i in range(len(avgError)):
    errorFile.write(str(avgError[i]))
    errorFile.write("\n")

errorFile.write(str(totalAvgError))

# ____________________________________________________FILTER__________________________________________________________ #
# find limits of acceptable frequency range
sortFreq = sorted(freq)
lowerLim = sortFreq[int((len(sortFreq)) / 2)] - freqRange
upperLim = sortFreq[int((len(sortFreq)) / 2)] + freqRange

# filter freq and gain using limits found
for i in range(len(freq)):
    if (freq[i] >= lowerLim) & (freq[i] <= upperLim):
        filtFreq.append(freq[i])
        filtGain.append(gain[i])
        filtDist.append(dist[i])
        filtTheta.append(theta[i])
        filtPhi.append(phi[i])

print("uniquePhi =", unique(filtPhi))
print("filtPhi =", filtPhi)
x = unique(filtTheta)
x.sort(reverse=True)
print("uniqueTheta =", x)
print("filtTheta =", filtTheta)

# _________________________________________________INTERPOLATION______________________________________________________ #
# duplicate the filtGain array
for i in range(len(filtGain)):
    filtGainFreq.append(filtGain[i])

# obtain the unique phi and theta angles
uniquePhi = unique(filtPhi)
uniqueTheta = unique(filtTheta)

uniqueTheta.sort(reverse=True)                              # organize angles from greatest to least (left to right)

# make list of gain measurements of the unique angles
for i in range(len(uniquePhi)):
    for j in range(len(filtPhi)):
        if filtPhi[j] == uniquePhi[i]:
            tempGainH.append(filtGain[j])
        if filtTheta[j] == uniqueTheta[i]:
            tempGainV.append(filtGain[j])

    # find the maximum gain for each unique angle in both horizontal and vertical radiation pattern
    maxGainH.append(max(tempGainH))
    maxGainV.append(max(tempGainV))

    # reset lists of gain measurements of the unique angles
    tempGainH = []
    tempGainV = []

x = len(filtPhi)

# interpolation
for i in range(len(maxGainH)):
    if i > 0:
        interpPoint = 0
        for j in range(len(maxGainH)):
            if interpPoint == 0:
                interpPoint = (maxGainH[i - 1] + maxGainH[i]) / 2
                if maxGainH[i] > maxGainH[i - 1]:
                    filtPhi.append(uniquePhi[i - 1] + 1)
                    filtGain.append(interpPoint)
                else:
                    filtPhi.append(uniquePhi[i] - 1)
                    filtGain.append(interpPoint)
            else:
                if maxGainH[i] > maxGainH[i-1]:
                    interpPoint = (interpPoint + maxGainH[i]) / 2
                    filtPhi.append(uniquePhi[i - 1] + (j + 1))
                    filtGain.append(interpPoint)
                else:
                    interpPoint = (interpPoint + maxGainH[i - 1]) / 2
                    filtPhi.append(uniquePhi[i] - (j + 1))
                    filtGain.append(interpPoint)

print("maxGainH =", maxGainH)
print(len(filtPhi[x:len(filtPhi)]))
print(filtPhi[x:len(filtPhi)])
print(filtGain[x:len(filtGain)])
print("final filtPhi =", filtPhi)
print(filtGain)

# __________________________________________________2D PLOTTING_______________________________________________________ #
# convert from degrees to radians to plot
for i in range(len(filtPhi)):
    filtPhi[i] = radians(filtPhi[i])
    #filtTheta[i] = radians(filtTheta[i])

#plt.figure(1)
#plt.polar(filtTheta, filtGain, 'o')

plt.figure(1)
plt.polar(filtPhi, filtGain, 'o')

print("filtGainFreq length =", len(filtGainFreq))
print("filtFreq length =", len(filtFreq))
# plot frequency vs. gain
plt.figure(2)
plt.plot(filtFreq, filtGainFreq, 'o')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Gain (dB)')
plt.title('Frequency (MHz) vs. Gain (dB)')
plt.show()

# __________________________________________________3D PLOTTING_______________________________________________________ #
THETA, PHI = np.meshgrid(filtTheta, filtPhi)

for i in range(len(filtGain)):                              # change gain from dB to Watts
    filtGain[i] = exp(filtGain[i]/10)

# convert from spherical to cartesian coordinates
R = filtGain                                                # _________________________NOTE___________________________ #
X = R * np.sin(PHI) * np.cos(THETA)                         # change THETA w/ PHI & PHI w/ THETA to see what you get!!!
Y = R * np.sin(PHI) * np.sin(THETA)
Z = R * np.cos(PHI)

# set parameters to plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
plot = ax.plot_surface(
    X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
    linewidth=0, antialiased=False, alpha=0.5
)

# Axes labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel(r'Power (W)')
plt.title('3D Plot')

plt.show()

# ______________________________________________________I/O___________________________________________________________ #
freqFile.close()
gainFile.close()
dtpFile.close()
errorFile.close()

# create the other two files that will need to be sent to create the radiation pattern
thetaFile = open("theta.txt", "w")
phiFile = open("phi.txt", "w")
for i in range(len(filtTheta)):
    thetaFile.write("%f\n" % filtTheta[i])
    phiFile.write("%f\n" % filtPhi[i])
thetaFile.close()
phiFile.close()
