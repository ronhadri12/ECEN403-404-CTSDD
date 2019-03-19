import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import math
from math import sin, cos, sqrt, atan2, radians, exp
import pdb


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

posAngle = False        # determine whether horizontal angle is pos or neg depending on normal vector of antenna
freqRange = 0.005       # acceptable maximum and minimum frequency range from median value of frequencies

# ______________________________________________________I/O___________________________________________________________ #
# read the files and store the parameters into corresponding lists
print("\nReading the files now.")
fFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\freqdata_022619.txt"
gFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\magdata_022619.txt"
gpsFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\coorddata_022619.txt"
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

for i in range(len(filtPhi)):
    filtPhi[i] = radians(filtPhi[i])
    filtTheta[i] = radians(filtTheta[i])

print(len(filtFreq))
print(len(filtGain))

# __________________________________________________2D PLOTTING_______________________________________________________ #
plt.figure(1)
plt.polar(filtTheta, filtGain, 'o')

plt.figure(2)
plt.polar(filtPhi, filtGain, 'o')

# plot frequency vs. gain
plt.figure(3)
plt.plot(filtFreq, filtGain, 'o')
plt.xlabel('Frequency (MHz)')
plt.ylabel('Gain (dB)')
plt.title('Frequency (MHz) vs. Gain (dB)')
plt.show()

# __________________________________________________3D PLOTTING_______________________________________________________ #
THETA, PHI = np.meshgrid(filtTheta, filtPhi)

for i in range(len(filtGain)):                              # change gain from dB to Watts
    filtGain[i] = exp(filtGain[i]/10)

# convert from spherical to cartesian coordinates
R = filtGain
X = R * np.sin(PHI) * np.cos(THETA)
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
ax.set_zlabel(r'Power (W)')

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
