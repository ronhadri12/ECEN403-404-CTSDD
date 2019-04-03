import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import math
from math import sin, cos, sqrt, atan2, radians, exp
import pdb
from scipy.interpolate import splprep, splev


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
thetaAng = []
GainH = []
GainV = []
Phi = []
Theta = []

# store maximum gain values in radiation pattern
maxGainH = []
maxGainV = []
tempGainH = []
tempGainV = []

filtGainFreq = []       # store gain values to compare to frequency
filtGainV = []          # store gain values to create vertical radiation pattern

posAngle = False        # determine whether horizontal angle is pos or neg depending on normal vector of antenna
freqRange = 0.001       # acceptable maximum and minimum frequency range from median value of frequencies
interpPointH = 0        # interpolated point at a certain angle for the HRP
interpPointV = 0        # interpolated point at a certain angle for the VRP

userLocation = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\";

# ______________________________________________________I/O___________________________________________________________ #
# read the files and store the parameters into corresponding lists
print("\nReading the files now.")
fFile = userLocation + "freqData_040119.txt"
gFile = userLocation + "magData_040119.txt"
gpsFile = userLocation + "coordData_040119.txt"
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

# _________________________________________________INTERPOLATION______________________________________________________ #
# duplicate the filtGain array
for i in range(len(filtGain)):
    filtGainFreq.append(filtGain[i])
    filtGainV.append(filtGain[i])

# obtain the unique phi and theta angles
uniquePhi = unique(filtPhi)
uniqueTheta = unique(filtTheta)

uniqueTheta.sort(reverse=True)                              # organize angles from greatest to least (left to right)

print("initial uniquePhi = ", uniquePhi)
print(len(uniquePhi))
print("initial uniqueTheta = ", uniqueTheta)
print(len(uniqueTheta))

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

# create 110 angle values in which 11 at a time are evenly spaced between two of the angles in uniqueTheta list
for i in range(len(uniqueTheta) - 1):
    thetaAngles = np.linspace(uniqueTheta[i], uniqueTheta[i + 1], 11)
    np.thetaAng = thetaAng.extend(thetaAngles)

# interpolation of horizontal radiation pattern
for i in range(len(maxGainH)):
    if i > 0:
        interpPointH = 0
        for j in range(len(maxGainH)):
            filtTheta.append(90)
            if interpPointH == 0:
                interpPointH = (maxGainH[i - 1] + maxGainH[i]) / 2
                if maxGainH[i] > maxGainH[i - 1]:
                    filtPhi.append(uniquePhi[i - 1] + 1)
                    uniquePhi.append(uniquePhi[i - 1] + 1)
                    filtGain.append(interpPointH)
                    GainH.append(interpPointH)
                    Phi.append(uniquePhi[i - 1] + 1)
                else:
                    filtPhi.append(uniquePhi[i] - 1)
                    uniquePhi.append(uniquePhi[i] - 1)
                    filtGain.append(interpPointH)
                    GainH.append(interpPointH)
                    Phi.append(uniquePhi[i] - 1)
            else:
                if maxGainH[i] > maxGainH[i - 1]:
                    interpPointH = (interpPointH + maxGainH[i]) / 2
                    filtPhi.append(uniquePhi[i - 1] + (j + 1))
                    uniquePhi.append(uniquePhi[i - 1] + (j + 1))
                    filtGain.append(interpPointH)
                    GainH.append(interpPointH)
                    Phi.append(uniquePhi[i - 1] + (j + 1))
                else:
                    interpPointH = (interpPointH + maxGainH[i - 1]) / 2
                    filtPhi.append(uniquePhi[i] - (j + 1))
                    uniquePhi.append(uniquePhi[i] - (j + 1))
                    filtGain.append(interpPointH)
                    GainH.append(interpPointH)
                    Phi.append(uniquePhi[i] - (j + 1))

# interpolation of vertical radiation pattern
for i in range(len(maxGainV)):
    if i > 0:
        interpPointV = 0
        for j in range(len(maxGainV)):
            filtPhi.append(0)
            if interpPointV == 0:
                interpPointV = (maxGainV[i - 1] + maxGainV[i]) / 2
                if maxGainV[i] > maxGainV[i - 1]:
                    filtTheta.append(thetaAng[thetaAng.index(uniqueTheta[i - 1]) + 1])
                    filtGain.append(interpPointV)
                    uniqueTheta.append(thetaAng[thetaAng.index(uniqueTheta[i - 1]) + 1])
                    GainV.append(interpPointV)
                    Theta.append(thetaAng[thetaAng.index(uniqueTheta[i - 1]) + 1])
                else:
                    filtTheta.append(thetaAng[thetaAng.index(uniqueTheta[i]) - 1])
                    filtGain.append(interpPointV)
                    uniqueTheta.append(thetaAng[thetaAng.index(uniqueTheta[i]) - 1])
                    GainV.append(interpPointV)
                    Theta.append(thetaAng[thetaAng.index(uniqueTheta[i]) - 1])
            else:
                if maxGainV[i] > maxGainV[i - 1]:
                    interpPointV = (interpPointV + maxGainV[i]) / 2
                    filtTheta.append(thetaAng[thetaAng.index(uniqueTheta[i - 1]) + (j + 1)])
                    filtGain.append(interpPointV)
                    uniqueTheta.append(thetaAng[thetaAng.index(uniqueTheta[i - 1]) + (j + 1)])
                    GainV.append(interpPointV)
                    Theta.append(thetaAng[thetaAng.index(uniqueTheta[i - 1]) + (j + 1)])
                else:
                    interpPointV = (interpPointV + maxGainV[i - 1]) / 2
                    filtTheta.append(thetaAng[thetaAng.index(uniqueTheta[i]) - (j + 1)])
                    filtGain.append(interpPointV)
                    uniqueTheta.append(thetaAng[thetaAng.index(uniqueTheta[i]) - (j + 1)])
                    GainV.append(interpPointV)
                    Theta.append(thetaAng[thetaAng.index(uniqueTheta[i]) - (j + 1)])

print(len(maxGainH))
print(len(maxGainV))
print(uniquePhi)
print(len(uniqueTheta))
GainH = maxGainH + GainH
GainV = maxGainV + GainV
print(len(GainH))
print(len(GainV))

# __________________________________________________2D PLOTTING_______________________________________________________ #
# convert from degrees to radians to plot
for i in range(len(filtPhi)):
    filtPhi[i] = radians(filtPhi[i])
    filtTheta[i] = radians(filtTheta[i])

for i in range(len(uniquePhi)):
    uniquePhi[i] = radians(uniquePhi[i])
    uniqueTheta[i] = radians(uniqueTheta[i])

plt.figure(1)
plt.polar(uniquePhi, GainH, 'o')

plt.figure(2)
plt.polar(uniqueTheta, GainV, 'o')

# plot frequency vs. gain
plt.figure(3)
plt.plot(filtFreq, filtGainFreq, 'o')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Gain (dB)')
plt.title('Frequency (MHz) vs. Gain (dB)')
plt.show()

# __________________________________________________3D PLOTTING_______________________________________________________ #
THETA, PHI = np.meshgrid(uniqueTheta, uniquePhi)
GAINH, GAINV = np.meshgrid(uniqueTheta, uniquePhi)

for i in range(len(filtGain)):                              # change gain from dB to Watts
    filtGain[i] = exp(filtGain[i]/10)

# convert from spherical to cartesian coordinates
R = GAINH * GAINV
X = R * np.sin(PHI) * np.cos(THETA)
Y = R * np.sin(PHI) * np.sin(THETA)
Z = R * np.cos(PHI)

# set parameters to plot
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
plot = ax.plot_surface(
    X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
    linewidth=1, antialiased=False, alpha=0.5
)

# Axes labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel(r'Power (W)')
plt.title('3D Plot')

print(len(filtGain))

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
