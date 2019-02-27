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
# specify which data set to analyze as the current one
dataSet = 3
BlakeDataSet = 5

# lists used to store radiation pattern parameters
listDistNums = []
listThetaNums = []
listPhiNums = []
dist = []
theta = []
phi = []
gain = []

freq = []       # list used to store all frequency values

errorList = []  # list used in percent error calculations

# filtered lists used to plot
filtFreq = []
filtGain = []
filtDist = []
filtTheta = []
filtPhi = []

# ______________________________________________________I/O___________________________________________________________ #
# read the files and store the parameters into corresponding lists
print("\nReading the files now.")
fFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\real_freqdata.txt"
gFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\real_magdata.txt"
gpsFile = "C:\\Users\\ronha\\OneDrive\\Documents\\Texas A&M\\Spring 2019\\ECEN 404-504\\sphereCoordData.txt"
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

    if i < 5:
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

        # lists of 11 elements with lists of 1024 elements
        #listDistNums = [DisThetaPhi[0]] * len(listFreqNums)
        #listThetaNums = [DisThetaPhi[1]] * len(listFreqNums)
        #listPhiNums = [DisThetaPhi[2]] * len(listFreqNums)

    # lists of 11 elements with lists of 1024 elements continued
    #gain.append(listGainNums)
    #freq.append(listFreqNums)
    #dist.append(listDistNums)
    #theta.append(listThetaNums)
    #phi.append(listPhiNums)

    # __________________________________________PERCENT ERROR CALCULATIONS____________________________________________ #
    if i > 0:
        errorNum = float(abs((listGainNums[i] - listGainNums[i - 1]) / listGainNums[i]))
        errorList.append(errorNum)
        if i == (file_len(gFile) - 1):
            errorFile.write(str(errorList))
            avgError = (sum(errorList) / len(errorList)) * 100

            # ______________________________________DISPLAY OUTPUT PARAMETERS_________________________________________ #
            print("Error =", errorList)
            print("Average error between gain measurements = %f" % avgError, "%")
            print("Distance list: ", dist)
            print("Theta list: ", theta)
            print("Phi list: ", phi)
            print("Gain list: ", gain)
            print("Frequency list: ", freq)

# ______________________________________________________I/O___________________________________________________________ #
freqFile.close()
gainFile.close()
dtpFile.close()
errorFile.close()

#print(len(gain[0]))
#print(len(freq))
#print(len(dist))
#print(len(theta[0]))
#print(len(phi[0]))

# ____________________________________________________FILTER__________________________________________________________ #
# find limits of acceptable frequency range
sortFreq = sorted(freq)
lowerLim = sortFreq[int((len(sortFreq)) / 2)] - 0.05
upperLim = sortFreq[int((len(sortFreq)) / 2)] + 0.05

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

#pdb.set_trace()                                             # breakpoint

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
#ax.set_xlabel(r'$\phi_\mathrm{real}$')
#ax.set_ylabel(r'$\phi_\mathrm{im}$')
#ax.set_zlabel(r'$V(\phi)$')

plt.show()

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

# create the other two files that will need to be sent to create the radiation pattern
thetaFile = open("theta.txt", "w")
phiFile = open("phi.txt", "w")
for i in range(len(theta)):
    thetaFile.write("%f\n" % theta[i])
    phiFile.write("%f\n" % phi[i])
thetaFile.close()
phiFile.close()
