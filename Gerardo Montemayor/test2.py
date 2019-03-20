from necpp import *
import math

def handle_nec(result):
  if (result != 0):
    print nec_error_message()

def monopole_impedance(freq, base, length):
  wavelength = 3e8/(1e6*freq)
  n_seg = int(math.ceil(50*length/wavelength))
  nec = nec_create()
  handle_nec(nec_wire(nec, 1, n_seg, 0, 0, base, 0, 0, base+length, 0.002, 1.0, 1.0))
  handle_nec(nec_geometry_complete(nec, 1, 0))
  handle_nec(nec_fr_card(nec, 0, 1, freq, 0))
  handle_nec(nec_ex_card(nec, 0, 0, n_seg/3, 0, 1.0, 0, 0, 0, 0, 0))
  handle_nec(nec_xq_card(nec, 0)) # Execute simulation
  # Results
  z = complex(nec_impedance_real(nec,0), nec_impedance_imag(nec,0))
  # Cleanup
  nec_delete(nec)
  return z

z = monopole_impedance(freq=134.5, base=0.1, length=4.0)
print "f=134.5 z = (%6.1f,%+6.1fI) Ohms" % (z.real, z.imag)
