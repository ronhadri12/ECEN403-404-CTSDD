import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import math
import cmath
from mpl_toolkits.mplot3d import Axes3D
pi = np.pi
theta = np.linspace(0,pi,180)
phi = np.linspace(0,2*pi,180)
theta,phi = np.meshgrid(theta,phi)
def vert(phi):
    return np.cos(phi)
mono = np.zeros(len(theta))
mono = vert(phi)
fig = plt.figure()
theoplot = fig.add_subplot(111,projection='3d')
ex = mono*np.sin(phi)*np.cos(theta)
ey = mono*np.sin(phi)*np.sin(theta)
#xe, ye, ze = sph2cart1(mag, theta, phi)
ez = mono*np.cos(phi)
#print(ex)
#print("\n")
#print(ey)
#print("\n")
#print(ez)
#stride=1,
theoplot.plot_surface(ex,ey,ez,rstride=1,cstride=1,cmap=plt.get_cmap('jet'),linewidth=1, antialiased=False, alpha=0.5)
plt.show()
