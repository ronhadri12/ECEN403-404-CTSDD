antenna_frequency = float(1500000000)

antenna_length = float(1)

wavelength = float(( 3 * (10 ** 8)) / antenna_frequency)

far_field = float((2 * (antenna_length ** 2)) / wavelength) # Far field calculation for antenna

print(far_field)
