# -*- coding: utf-8 -*-
"""
@author: Gerardo
"""

import numpy as np
from mayavi import mlab
import sys
import math
import cmath
import numpy as np
import matplotlib as plt
from mpl_toolkits.mplot3d import Axes3D
plt.use('TkAgg')

#import all text into arrays
##import theoretical
#theoretical = open('theoretical.txt','r')
#measured = open('measured.txt','r')

pi = np.pi
N = 6
c = 3e8
f = 1700e6
omega = 2*pi*f
wl = c/f
B = (2*pi)/wl
d = 0.5*wl
dt = 0.5*wl
e = 1/(36*pi*1e9)
mu = 4*pi*1e-7
theo = []
meas = []
#input receving, to be formatted
"""
tharrdata = []
mearrdata = []
holder = ""


for line in theoretical:
    theo = line.split()
    tharrdata.append(theo)
    theo = []


for line in measured:
    meas = line.split()
    mearrdata.append(meas)
    meas = []
measrad = []
theorad = []
measrad[1:] = np.deg2rad(meas[1:])
theorad[1:] = np.deg2rad(theo[1:])
measrad[2:] = meas[2:]
theorad[2:] = theo[2:]
measrad[3:] = meas[3:]
theorad[3:] = theo[3:]

create function for data point averaging, in case of faulty/spotty data
"""


theta = np.linspace(0,pi,180)
phi = np.linspace(0,pi,180)

#determine phase shift from angle
def antennaphase(angle):
    angrad = np.deg2rad(angle)
    alpha = (-1)*B*d*(math.cos(angrad))
    return alpha

#pattern functions

def psi(B, d, theta, angle):
    a = B*d*np.cos(theta) + antennaphase(angle)
    return a

def antfunc(B, d, theta, angle, N):
    a = np.sin(N*0.5*psi(B, d, theta, angle))
    b = N*np.sin(0.5*psi(B,d,theta,angle))
    return (a/b)


def theofunction(theta):
    a = np.sin(2.88*(pi)*np.cos(theta))
    b = np.sin(0.72*pi*np.cos(theta))
    return (a/b)

def testfunc(theta):
    a = np.sin(2.4*(pi)*np.cos(theta))
    b = np.sin(0.6*pi*np.cos(theta))
    return (a/b)

def testfunc2(theta):
    a =  np.sin(2.4*(pi)*np.cos(theta)-1.69706*pi)
    b = 4*np.sin(0.6*pi*np.cos(theta)-0.424264*pi)
    return (a/b)

#thearrdata = np.concatenate(theta,theofunction(theta))
#print(thearrdata)

def loadData(array, function):
    data = np.arange(array.size)
    data = function(array)
    return data

def horfunction(phi):
	return (((np.sin(phi))**0.45))


hordata = np.arange(phi.size)
hordata = horfunction(theta)


#maximum parameter functions
def maxmagnang(array,function):
    mag = -1000000
    ang = 0

    for g in range(array.size) :
        if mag < function(array).item(g):
            mag = function(array).item(g)
            ang = g

    return mag, ang
thmag, thang = maxmagnang(theta,theofunction)
memag, meang = maxmagnang(theta,testfunc)


def sumfunc(N,d):
    sa = []
    for m in range(1,N+1):
        sa.append(((N-m)/(m*B*d))*np.sin(m*B*d))
    dsum = sum(sa)
    print(dsum)
    return dsum

#max directivity

def Directivity(N,d):
    D = 1/(1/N + (2/(N**2))*sumfunc(N,d))
    #print("Directivity number: ")
    #print(D)
    return D

Dt = 1/(1/N + (2/(N**2))*sumfunc(N,d))
Dm = 1/(1/N + (2/(N**2))*sumfunc(N,dt))
#with phase shift
#Dm = ((np.sin(0.))/())/(1/N + (2/(N**2))*sumfunc(N,dt))


#percentage error of directivity
def pererr(th,me):

    return (abs(th - me))/(th)

dd = abs(Dt - Dm)
pedd = dd/Dt


#percentage error of db and angle of max point
dmag = abs(thmag - memag)
dang = abs(thang - meang)

pemag = dmag/thmag
peang = dang/thang




#plotting
#print(theodata)
#fig = plt.pyplot.figure()
#theoplot = fig.add_subplot(111,projection='3d')
theta, phi = np.meshgrid(theta,phi)
mag = abs(theofunction(theta))*horfunction(phi)
mag = 20*np.log10(mag)
#ex, ey, ez = sph2cart1(mag, theta, phi)
ex = mag*np.sin(phi)*np.cos(theta)
ey = mag*np.sin(phi)*np.sin(theta)
ez = mag*np.cos(phi)
#theoplot.plot_surface(ex,ez,ey,rstride=1,cstride=1,cmap=plt.pyplot.get_cmap('jet'),linewidth=1, antialiased=False, alpha=0.5)

#plt.pyplot.show()

src = mlab.pipeline.array2d_source(mag)
warp = mlab.pipeline.warp_scalar(src)
normals = mlab.pipeline.poly_data_normals(warp)
surf = mlab.pipeline.surface(normals)
mlab.show()

#add
#3dplot = fig.add_subplot(212, projection='3d')
#3dplot.scatter(theta)


#max current
def maxA(maxE):
    return (maxE*4*pi)/(omega*mu)

##SLL Tracking

def slltrack(x):
    lobes = np.array([0.0],dtype='float')
    left = np.array([0.0,0.0],dtype='float')
    mid = np.array([0.0,1.0],dtype='float')
    right = np.array([0.0,2.0],dtype='float')

    while right[1]!=360:
        left.put(0,x.item(int(left.item(1))))

        #print(left.item(0))

        mid.put(0,x.item(int(mid.item(1))))


        right.put(0,x.item(int(right.item(1))))

        if (math.floor(mid.item(0)/right.item(0))>1 and math.floor(mid.item(0)/left.item(0))>1) == 1:
            print('true')

        #print(right.item(0))
        if math.floor(mid.item(0)/right.item(0))>1 and math.floor(mid.item(0)/left.item(0))>1:
            np.append(lobes,mid)

        left[1] = mid[1]
        mid[1] = right[1]
        right[1] = right[1] + 1

    #print(lobes)
    return lobes
#slltest = slltrack(theodata)
##respond to errors in measurement to user
##more current to antenna
##redirect antenna (reorient)
##check spacing - sll
##check that current is evenly distributed among antenna feedpoints
print('Program finished')
if pemag>0.05:
    print('Please increase current to antenna, antenna current is currently {}A, theoretical antenna current is {}A:'.format(maxA(memag),maxA(thmag)))
if peang>0.05:
    print('Please reorient array by :{}° to the {}'.format((dang), 'right' if(thang-meang)>0 else 'left'))
if pedd>0.1:
    print('Please check element spacing, current theoretical spacing: {}m, current spacing: {}m'.format(d,dt))
if peang>0.05 and pedd>0.01:
    print('Please check the current is evenly distributed to all array elements')
