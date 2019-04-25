# from __future__ import division
# from __future__ import unicode_literals
# coding=utf-8
# -*- coding: utf-8 -*-
"""
@author: Gerardo
"""
import sys
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
pi = np.pi
angle = 90
N = 4
c = 3e8
f = 433e6
omega = 2*pi*f
wl = c/f
B = (2*pi)/wl
d = 0.72*wl
dt = 0.72*wl
e = 1/(36*pi*1e9)
mu = 4*pi*1e-7
alpha = 0
selections = np.zeros(5)
def angleloader(numberofitems):
    theta = np.linspace(pi/3,(2/3)*pi,numberofitems)
    phi = np.linspace(pi/3,(2/3)*pi,numberofitems)
    return theta, phi

def horfunction(phi):
    return (((np.sin(phi))**0.45))

#load theta and phi values onto numpy arrays
theta, phi = angleloader(121);

#hordata = np.arange(phi.size)
hordata = horfunction(theta)

#functions
def parameterloading(selections):
    if selections[0] == 1 :
        if selections[1] != 0:
            alpha = selections[1]
        if selections[2] != 0:
            N = selections[2]
        if selections[3] != 0 :
            d = selections[3]*wl
        if selections[4] != 0 :
            wl = c/(selections[4])
    return 0

def maxmagnang(array):
    mag = -1000000.0000
    ang = 0
    for g in range(array.size) :
        if mag < array.item(g):
            mag = array.item(g)
            ang = g
    return mag, ang

#determine phase shift from angle
def antennaphase(angle):
    angrad = np.deg2rad(angle)
    alpha = (-1)*B*d*(math.cos(angrad))
    return alpha

#pattern functions
def psi(B, d, theta, angle):
    a = B*d*np.cos(theta) + antennaphase(angle)
    return a

def antfunc(w = B, x = 1.5*d, y = theta, z = angle, z1 = N):
    a = np.sin(z1*0.5*psi(w, x, y, z))
    b = z1*np.sin(0.5*psi(w,x,y,z))
    return (a/b)


def theofunction(theta):
    a = np.sin(2.88*(pi)*np.cos(theta))
    b = N*np.sin(0.72*pi*np.cos(theta))
    return (a/b)

def testfunc(theta):
    a = np.sin(2.4*(pi)*np.cos(theta))
    b = N*1000*np.sin(0.6*pi*np.cos(theta))
    return (a/b)

def testfunc2(theta):
    a =  np.sin(2.4*(pi)*np.cos(theta)-1.69706*pi)
    b = 4*np.sin(0.6*pi*np.cos(theta)-0.424264*pi)
    return (a/b)



def sumfunc(N,d):
    sa = 0
    for m in range(1,N-1):
        sa = sa + ((N-m)/(m*B*d))*np.sin(m*B*d)*np.cos(m*alpha)
    #print(sa)
    return sa

#percentage error testing
def pererr(th,me,angs,fig):
    if th.size == me.size:
        perrs = np.zeros(th.size)
        arr = th
        arr = arr.astype(int)
        for i in range(th.size):
            #print(th[i] - me[i])
            #print((abs(th[i] - me[i]))/(th[i]))
            perrs[i] = (abs(th[i] - me[i]))/(th[i])
    theoplot = fig.add_subplot(111,projection='polar')
    theoplot.plot(angs, perrs ,color='orange',label='Percentage Error')
    theoplot.legend()
    #plt.show()
    return perrs

#max directivity
def Directivity(N,d):
    zn = 0
    if sumfunc(N,d) > 1e-5:
        zn = (2/(N**2))*sumfunc(N,d)

    D = 1/((1/N) + zn)
    return D

#max current
def maxA(maxE):
    return (maxE*4*pi)/(omega*mu)

#SLL Tracking

def slltrack(arrayfunction, theta):
    test = abs(arrayfunction)
    #test = np.asarray(test)
    sll = np.zeros(test.size)
    arr = np.linspace(1,test.size,test.size)
    arr = arr.astype(int)
    for x in arr:
        if int( x + 1 ) < int(test.size) :
            if (test.item(x-1) < test.item(x)) and (test.item(x) > test.item(x+1)) :
                #print(test.item(x-1),test.item(x),test.item(x+1))
                sll[x] = test.item(x)
    #print(sll)
    fig = plt.figure()
    plt.ion()
    theoplot = fig.add_subplot(111,projection='polar')
    theoplot.scatter(theta,arrayfunction,color='red',label='Data')
    theoplot.scatter(theta, sll, color='blue',label='Lobe Positions')
    theoplot.legend()
    plt.show()
    return 0



def tdp(angs,theofun,mesfun,Dt,Dm,thmag,thang,memag,meang):
        fig = plt.figure()
        plt.ion()
        theoplot = fig.add_subplot(111,projection='polar')
        #theoplot = plt.subplot(111,polar=True)
        #theoplot.scatter(theta, theofunction(theta), color='blue', label='Theoretical')
        theoplot.scatter(angs, theofun, color='blue', label='Theoretical')
        theoplot.scatter(angs, mesfun, color='red', label='Measured')
        theoplot.legend()
        theoplot.text(0.6,1.5,'Theoretical Directivity: {}'.format(Dt))
        theoplot.text(0.55,1.5,'Measured Directivity: {}'.format(Dm))
        theoplot.text(0.5,1.5,'Theoretical Max Magnitude: {}'.format(thmag))
        theoplot.text(0.45,1.5,'Theoretical Max Angle: {}'.format(thang))
        theoplot.text(0.4,1.5,'Measured Max Magnitude: {}'.format(memag))
        theoplot.text(0.35,1.5,'Measured Max Angle: {}'.format(meang))
        #pererr(theofun,mesfun,angs,fig)
        plt.show()
        return fig

def trdp(theta = theta, phi = phi,antfunc = antfunc, B = B, d = d, angle = angle, N = N, horfunction = horfunction):
        fig = plt.figure()
        plt.ion()
        theoplot = fig.add_subplot(111,projection='3d')
        theta, phi = np.meshgrid(theta,phi)
        # print(theta.shape)
        # print(phi.shape)
        tester = abs(antfunc(B, 1.5*d, theta, angle, N))
        #tester = 20*np.log10(tester)
        mag = tester*horfunction(phi)
        tx = mag*np.sin(phi)*np.cos(theta)
        ty = mag*np.sin(phi)*np.sin(theta)
        tz = mag*np.cos(phi)
        theoplot.plot_surface(tx,tz,ty,rstride=1,cstride=1,cmap=plt.get_cmap('jet'),linewidth=1, antialiased=False, alpha=0.5);
        plt.show();
        return 0

def fixer(pemag,peang,pedd,memag,thmag,dang,thang,meang,d,dt):
        ##respond to errors in measurement to user
        ##more current to antenna
        ##redirect antenna (reorient)
        ##check spacing - sll
        ##check that current is evenly distributed among antenna feedpoints

        if pemag>0.05:
            print('Please increase current to antenna, antenna current is currently {}A, theoretical antenna current is {}A:'.format(maxA(memag),maxA(thmag)))
        if peang>0.05:
            print('Please reorient array by :{}, {}'.format(((180/pi)*dang), 'upwards' if(dang)>0 else 'downwards'))
        if pedd>0.1:
            print('Please check element spacing, current theoretical spacing: {}m, current spacing: {}m'.format(d,dt))
        if peang>0.05 and pedd>0.01:
            print('Please check the current is evenly distributed to all antenna array elements')
            return 0

def maindef(mesPhi, mesTheta, mesH, mesV,selections):
    mesPhi = np.asarray(mesPhi)
    mesTheta = np.asarray(mesTheta)
    mesH = np.asarray(mesH)
    mesV = np.asarray(mesV)

    parameterloading(selections)



    #maximum parameter functions
    thmag, thang = maxmagnang(antfunc())
    memag, meang = maxmagnang(mesH)
    thang = theta.item(thang)
    #print(thang)
    meang = theta.item(meang)
    #print(meang)
    #test with rons data

    Dt = Directivity(N,d)
    #print(Dt)
    Dm = Directivity(N,d)
    #print(Dm)
    #with phase shift
    #Dm = ((np.sin(0.))/())/(1/N + (2/(N**2))*sumfunc(N,dt))


    #percentage error of directivity
    dd = abs(Dt - Dm)
    pedd = dd/Dt
    #percentage error of db and angle of max point
    dmag = abs(thmag - memag)
    dang = thang - meang
    pemag = dmag/thmag
    peang = abs(dang)/thang
    #pererr(theofunction(theta),mesV,theta)
    #pererr((horfunction(phi))/7,mesH,phi)
    #track sll and main lobes
    slltest = slltrack(antfunc(), theta)
    slltest2 = slltrack(mesV,theta)
    fig2 = tdp(theta,thmag*(antfunc()),mesV,Dt,Dm,thmag,thang,memag,meang)
    fig3 = tdp(phi,memag*(horfunction(phi)),mesH,Dt,Dm,thmag,thang,memag,meang)
    pererr((horfunction(phi))*memag,mesH,phi,fig3)
    pererr((antfunc())*thmag,mesH,phi,fig2)

    trdp(theta, phi, antfunc, B, d, angle, N, horfunction)
    fixer(pemag,peang,pedd,memag,thmag,dang,thang,meang,d, dt)

    return 0
