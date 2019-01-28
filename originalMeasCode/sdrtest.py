# This is the original file/code for sdrdata.py.

from pathlib2 import Path
from pylab import psd, xlabel, ylabel, show
from rtlsdr import RtlSdr
# import numpy as np

# define write function
def write_data(data_points, magnitude, frequency, mag_file, freq_file):
    i = 0
    mag_file.write('[')
    freq_file.write('[')
    while i < data_points-1:
        mag_file.write("%s, " % magnitude[i])
        freq_file.write("%s, " % frequency[i])
        i += 1
    mag_file.write('%s]\n' % magnitude[i])
    freq_file.write('%s]\n' % frequency[i])
    return;

sdr = RtlSdr()
# np.set_printoptions(threshold=np.inf)

# configure device
sdr.sample_rate = 2.4e6      # Hz
sdr.center_freq = 95.1e6       # Hz
sdr.freq_correction = 60  # PPM
sdr.gain = 4 # 'auto'

# extract data
data_points = 1024
data = sdr.read_samples(256*data_points)

# initialize
samples = sdr.read_samples(256*data_points)
mag_file_path = '/home/pi/magtest.txt'
freq_file_path = '/home/pi/freqtest.txt'

sdr.close()

# PSD plot
psddata = psd(samples, NFFT=data_points, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
#xlabel('Frequency (MHz)')
#ylabel('Relative power (dB)')
#show()

magnitude = psddata[0]
frequency = psddata[1]

# write data
# magnitude has not been converted to dB yet. To convert, 10*log(magnitude)
if Path(mag_file_path).is_file() and Path(freq_file_path).is_file():
    with open(mag_file_path, 'a') as mag_file, open(freq_file_path, 'a') as freq_file:
        write_data(data_points, magnitude, frequency, mag_file, freq_file)
#        i = 0
#        mag_file.write('[')
#        freq_file.write('[')
#        while i < data_points-1:
#            mag_file.write("%s, " % magnitude[(i)])
#            freq_file.write("%s, " % frequency[(i)])
#            i += 1
#        mag_file.write('%s]\n' % magnitude[i])
#        freq_file.write('%s]\n' % frequency[i])
        #for mag_item in magnitude:
        #    mag_file.write("%s, " % mag_item)
else:
    with open(mag_file_path, 'w') as mag_file, open(freq_file_path, 'w') as freq_file:
        write_data(data_points, magnitude, frequency, mag_file, freq_file)
#        i = 0
#        mag_file.write('[')
#        freq_file.write('[')
#        while i < data_points-1:
#            mag_file.write("%s, " % magnitude[i])
#            freq_file.write("%s, " % frequency[(i)])
#            i += 1
#        mag_file.write('%s]\n' % magnitude[i])
#        freq_file.write('%s]\n' % frequency[i])

# testfile = open(path, "w")
# testfile.write(str(magnitude))
# testfile.write(str(frequency))
# testfile.close()


# output
print(data)
print(psddata)
print(magnitude)
print(frequency)
print(len(magnitude))
print(len(frequency))

xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')
show()