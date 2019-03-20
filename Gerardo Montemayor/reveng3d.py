# -*- coding: utf-8 -*-
"""
@author: Gerardo
"""
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 


#import all text into arrays
##import theoretical
#theoretical = open('theoretical.txt','r')
#measured = open('measured.txt','r')

def sph2cart1(r,th,phi):
     x=r*np.cos(th)*np.sin(phi)
     y=r*np.sin(th)*np.sin(phi)
     z=r*np.cos(phi);
     return x,y,z


pi = np.pi
N = 4
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


theta = np.linspace(0,2*pi,90)
phi = np.linspace(0,2*pi,90)

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
    #funcret = np.empty([1,360])
    a = np.sin(N*0.5*psi(B, d, theta, angle))
    b = N*np.sin(0.5*psi(B,d,theta,angle))
    #funcret[:] = (a/b)
    return (a/b)


def theofunction(theta):
    #funcres=np.empty([1,360])
    a = np.sin(2.88*(pi)*np.cos(theta))
    b = np.sin(0.72*pi*np.cos(theta))
    #funcres[:] = (a/b)
    return a/b

def testfunc(theta):
    #funcres=np.empty([1,360])
   # for i in theta:
    a = np.sin(2.4*(pi)*np.cos(theta))
    b = np.sin(0.6*pi*np.cos(theta))
    #funcres[:] = (a/b)

    return (a/b)

def testfunc2(theta):
    #funcres = np.empty([1,360])
    #for i in theta:
    a =  np.sin(2.4*(pi)*np.cos(theta)-1.69706*pi)
    b = 4*np.sin(0.6*pi*np.cos(theta)-0.424264*pi)
    #funcres[:] = (a/b)

    return (a/b)

#thearrdata = np.concatenate(theta,theofunction(theta))
#print(thearrdata)

def loadData(array):
    return
#load arrays with data for plotting
theodata = np.arange(360)
theodata = theofunction(theta)

medata = np.arange(360)
medata = testfunc(theta)

def horfunction(theta):
	#funcres = np.empty([1,360])
	#funcres[:] = ((np.sin(theta))**0.45)*0.25
	return (((np.sin(theta))**0.45))


hordata = np.arange(360)
hordata = horfunction(theta)

#3D function
def totaldat(mesher):
#z = np.empty([mesher.size()])
	return


def maxmag(array):
    return
def maxang(array):
    return

#maximum parameter functions
thmag = -1000000
thang = 0

memag = -1000000
meang = 0

for g in range(90) :
    if thmag < theodata.item(g):
        thmag = theodata.item(g)
        thang = g

    if memag< medata.item(g):
        memag = medata.item(g)
        meang = g

def sumfunc(N,d):
    sa = []
    for m in range(1,N+1):
        sa.append(((N-m)/(m*B*d))*math.sin(m*B*d))
    dsum = sum(sa)
    return dsum

#max directivity

def Directivity(N,d):
    D = 1/(1/N + (2/(N**2))*sumfunc(N,d))
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
fig = plt.figure()
theoplot = fig.add_subplot(111,projection='3d')

mag = np.outer(abs(horfunction(theta)),abs(theofunction(theta)))
x = mag*abs(np.sin(theta)*np.cos(phi))
y = mag*abs(np.sin(theta)*np.sin(phi))
#xe, ye, ze = sph2cart1(mag, theta, phi) 
z = abs(mag*np.cos(theta))
theoplot.plot_wireframe(x,y,z,stride=1, cstride=1, cmap=plt.get_cmap('jet'),linewidth=0, antialiased=False, alpha=0.5)
#theoplot = plt.subplot(111,polar=True)
#theoplot.scatter(theta, theofunction(theta), color='blue', label='Theoretical')
#theoplot.scatter(theta, theodata, color='blue', label='Theoretical')
#theoplot.scatter(theta, hordata, color='red', label='hor')
#theoplot.scatter(theta, testfunc(theta), color = 'red', label='Measured')
#theoplot.legend()
#theoplot.text(0.6,1.5,'Theoretical Directivity: {}'.format(Dt))
#theoplot.text(0.55,1.5,'Measured Directivity: {}'.format(Dm))
#theoplot.text(0.5,1.5,'Theoretical Max Magnitude: {}'.format(thmag))
#theoplot.text(0.45,1.5,'Theoretical Max Angle: {}'.format(thang))
#theoplot.text(0.4,1.5,'Measured Max Magnitude: {}'.format(memag))
#theoplot.text(0.35,1.5,'Measured Max Angle: {}'.format(meang))
plt.show()
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
