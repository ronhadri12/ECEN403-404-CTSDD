# This file contains the functions necessary for collecting data.

# To import this function file, measurements.py, move it so that it is
# located in the same directory and include the following line in the
# main code:
# import measurements.py as FILE
# replacing FILE with an appropriate file name. To call functions from
# the main code, use the following:
# FILE.function(a, b)

# Used for GPS data collection
# from dronekit import connect

# Used for signal data collection
from pylab import psd
from rtlsdr import RtlSdr

# Used for both GPS and signal data collection
from pathlib2 import Path 



# GPS data collection function
# import into point_set_func, but will be copied into flight_control_1 anyways
def saveGPS(lat_data, lon_data, alt_data, file_path):
    vehicle = connect("/dev/ttyS0", wait_ready = True, baud = 921600)

    # Directory to store GPS data
    gps_file_path = file_path + "/gpsdata.txt"

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
def saveSignal(freq, file_path):
    # Define function for writing signal data into file
    def write_data(data_points, magnitudeData, frequencyData, mag_file, freq_file):
        i = 0
        mag_file.write('[')
        freq_file.write('[')
        while i < data_points-1:
            mag_file.write("%s, " % magnitudeData[i])
            freq_file.write("%s, " % frequencyData[i])
            i += 1
        mag_file.write('%s]\n' % magnitudeData[i])
        freq_file.write('%s]\n' % frequencyData[i])

    sdr = RtlSdr()

    # Configure SDR
    sdr.sample_rate = 2.4e6        # Hz
    sdr.center_freq = freq         # Hz
    sdr.freq_correction = 60       # PPM
    sdr.gain = 4                   # 'auto'

    # Initialize
    data_points = 1024
    samples = sdr.read_samples(256*data_points)
    mag_file_path = file_path + "/magdata.txt"
    freq_file_path = file_path + "/freqdata.txt"

    ### *** IMPORTANT *** (for later, when optimizing)
    ### I'm not sure if we should leave this outside of the function
    ### and move it to the end of the main code, after the flight path
    ### ends. Idk the impact of leaving the SDR open/on for an extended
    ### period of time. If we move sdr.close() outside, we have to
    ### remember to also move the above code outside as well.
    ### Leaving this line within this function should be fine for now.
    sdr.close()

    # PSD plot data
    psddata = psd(samples, NFFT=data_points, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)

    # Extracting pertinent information from the PSD plot calculation
    magnitudeData = psddata[0]
    frequencyData = psddata[1]

    # Check for .txt file and write data
    # For Ron: Magnitude has not been converted to dB yet. To convert, 10*log(magnitude).
    if Path(mag_file_path).is_file() and Path(freq_file_path).is_file():
        with open(mag_file_path, 'a') as mag_file, open(freq_file_path, 'a') as freq_file:
            write_data(data_points, magnitudeData, frequencyData, mag_file, freq_file)
    else:
        with open(mag_file_path, 'w') as mag_file, open(freq_file_path, 'w') as freq_file:
            write_data(data_points, magnitudeData, frequencyData, mag_file, freq_file)
    
    print("Data saved successfully.")



# CHANGELOG

# Feb 9, 2018
# Cleared up a few comments/notes to self and cleaned up code in [measurements.py]

# Feb 10, 2018
# Verified exchangeable formatting for sdr.center_freq (95.1e6 vs 95100000 vs 95100000.0)
# Added ability to allow user to choose save location [in Flight_Control_v2.py]
# Made code more robust by preventing user from inputting invalid arugments [in Flight_Control_v2.py]

# Feb 11, 2018
# Renamed functions from collectBlah to saveBlah for clarity
# Added ability to configure center frequency of SDR
# Modified saveSignal to save data dynamically based off of user input
# Added data save confirmation for verification
# Modified saveGPS to save data dynamically based off of user input