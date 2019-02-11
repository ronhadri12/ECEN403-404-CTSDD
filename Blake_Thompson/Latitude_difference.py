
import scipy.integrate as integrate
import math

lat = 30.59

lower_lat = math.floor(lat)     #finds the latitude line above the current location
upper_lat = math.ceil(lat)      #finds the latitude line below the current location

polar_lower_lat = (lower_lat * math.pi) / 180
polar_upper_lat = (upper_lat * math.pi) / 180

lower_angle = (math.atan((6378137.0/6356752.0) * math.tan(polar_lower_lat)))
upper_angle = (math.atan((6378137.0/6356752.0) * math.tan(polar_upper_lat)))



test_lower = lower_angle / math.pi
test_upper = upper_angle / math.pi




def integrand(x):
    return math.sqrt(((6378137**2) * ((math.sin(x))**2)) + ((6356752**2) * ((math.cos(x))**2)))

Y = integrate.quad(integrand, lower_angle, upper_angle)                   # Integral to find the arc length between latitiude lines of the earth

print(Y)
