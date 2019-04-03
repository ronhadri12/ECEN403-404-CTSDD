from __future__ import division
from __future__ import unicode_literals
# coding=utf-8
# -*- coding: utf-8 -*-
"""
@author: Gerardo
"""
from database import maindef
from dataproc import mainfun
import sys
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
print("Welcome to the CTSDD Project")
print("Created by Blake Thompson, Josh Suen, Ron Hadri and Gerardo Montemayor")
print("Please select one of the following options:")
print("1) Configure Theoretical Array Pattern (angle, number of array elements, element spacing, horiozontal angle)")
print("2) Plot using default values")
#print("3) Determine errors between measured and theoretical")
#print("4) ")
print("5) ")
print("Press q to quit ")
inp = ""
while inp != "q":
    inp = str(input("Please input your choice: "))
    if inp == "2":
        pass
    if inp == "2":
        mesG, mesT, mesP = mainfun()
        maindef(mesG, mesT, mesP)
