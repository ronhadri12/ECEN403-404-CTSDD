from __future__ import division
from __future__ import unicode_literals
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

def inter(g,h,x):
    a = data.item(g)
    b = data.item(h)
    #y = np.array([b - a*np.exp((-1)*x*(b/a))])
    #print(y)
    if b>a:
        y = b - a*np.exp((-0.35)*x)
        if y<1:
            print(y)
            print(x)
            print(g)
            print(h)
            return 0
        return y
    else:
        y = a - b*np.exp((0.35)*((data.size-1)*x))
        if y<1:
            print(y)
            print(x)
            print(g)
            print(h)
            return 0
        return y

data = np.array([1,2,3,4,5,6,5,4,3,2,1])
angs = np.array([300,312,324,336, 348, 0, 12, 24, 36, 48, 60])
totdata = np.array([])
for num in range(data.size):
    if num+1<data.size:
        temp = np.empty([1,1])
        max = int(math.floor((121-data.size)/11))
        for nums in range(max):
            temp2 = np.array([inter(num,num+1,nums)])
            temp = np.append(temp,temp2)
        totdata = np.append(totdata,data.item(num))
        totdata = np.append(totdata,temp)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(range(120),totdata)
plt.show()
