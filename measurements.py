### *** IMPORTANT ***
### I'm not sure if these libraries need to be imported here, in the 
### function file, or if they need to be imported in the main file.
### You can just cut and paste if it's the latter. If you import this
### function file instead of individual functions then I think it's
### the former, where the libraries only need to be imported here.

# *** IMPORTANT ***
# The file importing this file, measurements.py, must be located in
# the same directory as this file.

# This is the file containing all functions necessary for collecting
# data. The code for each function is from the files gpstest.py and
# sdrtest.py. The code from gpstest.py has been edited to accept
# parameters.

# To import this function file, measurements.py, include the following
# line in the main code:
# import measurements.py as FILE
# replacing FILE with an appropriate file name. To call functions from
# the main code, use the following:
# FILE.function(a, b)

# Used for GPS data collection
from dronekit import connect

# Used for signal data collection
from pylab import psd
from rtlsdr import RtlSdr

# Used for both GPS and signal data collection
from pathlib2 import Path 



# GPS data collection function
def collectGPS(lat_data, lon_data, alt_data):
    vehicle = connect("/dev/ttyS0", wait_ready = True, baud = 921600)

    # Directory to store GPS data
    gps_file_path = '/home/pi/gpsdata.txt' 

    # *** IMPORTANT ***
    # The following 3 lines of code that have been commented out
    # must be added to the main code. The variable names do not
    # need to be the same.
    # lat_data = vehicle.location.global_frame.lat
    # lon_data = vehicle.location.global_frame.lon
    # alt_data = vehicle.location.global_frame.alt

    # Check for .txt file and write data
    if Path(gps_file_path).is_file():
        with open(gps_file_path, 'a') as gps_file:
            gps_file.write('[%s, %s, %s], ' % (lat_data, lon_data, alt_data))
    else:
        with open(gps_file_path, 'w') as gps_file:
            gps_file.write('[%s, %s, %s], ' % (lat_data, lon_data, alt_data))
            
            
            
# Signal data collection function
def collectSignal():
    # Define function for writing signal data into file
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

    sdr = RtlSdr()

    ### IDK what freq_correction does or how sample_rate and gain affect
    ### the measurements (they affect it, I just don't know how) :)
    # Configure SDR
    sdr.sample_rate = 2.4e6        # Hz
    sdr.center_freq = 95.1e6       # Hz
    sdr.freq_correction = 60       # PPM
    sdr.gain = 4                   # 'auto'

    # Initialize
    data_points = 1024
    samples = sdr.read_samples(256*data_points)
    mag_file_path = '/home/pi/magdata.txt'
    freq_file_path = '/home/pi/freqdata.txt'

    ### *** IMPORTANT *** (for later, when optimizing)
    ### I'm not sure if we should leave this outside of the function
    ### and move it to the end of the main code, after the flight path
    ### ends. Idk the impact of leaving the SDR open/on? for an extended
    ### period of time. If we move sdr.close() outside, we have to
    ### remember to also move the above code outside as well.
    ### Leaving this line within this function should be fine for now.
    sdr.close()

    # PSD plot data
    psddata = psd(samples, NFFT=data_points, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

    # Extracting pertinent information from the PSD plot calculation
    magnitude = psddata[0]
    frequency = psddata[1]

    # Check for .txt file and write data
    # Magnitude has not been converted to dB yet. To convert, 10*log(magnitude). This comment is for Ron.
    if Path(mag_file_path).is_file() and Path(freq_file_path).is_file():
        with open(mag_file_path, 'a') as mag_file, open(freq_file_path, 'a') as freq_file:
            write_data(data_points, magnitude, frequency, mag_file, freq_file)
    else:
        with open(mag_file_path, 'w') as mag_file, open(freq_file_path, 'w') as freq_file:
        write_data(data_points, magnitude, frequency, mag_file, freq_file)