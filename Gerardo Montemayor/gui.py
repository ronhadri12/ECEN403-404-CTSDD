# from __future__ import division
# from __future__ import unicode_literals
# coding=utf-8
# -*- coding: utf-8 -*-
"""
@author: Gerardo
"""
import database
import dataproc
from database import maindef
from dataproc import mainfun
import sys
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
inp = ""
selections = np.zeros(5)
selections = selections.astype(int)
opt = ""
print("\n")
print("Welcome to the CTSDD Project")
print("Created by Blake Thompson, Josh Suen, Ron Hadri and Gerardo Montemayor")
while inp != "q":
    print("\n")
    print("Please select one of the following options:")
    print("1) Configure Theoretical Array Pattern (angle, number of array elements, element spacing, frequency)")
    print("2) Run the database using theoretical and measured points")
    print("3) Plot 3D Theoretical Model")
    print("4) Plot 3D Measured Model")
    print("Press q to quit ")
    print("\n")
    inp = str(input("Please input your functionality choice: "))
    if inp == "1":
        while opt != "q":
            print("\n")
            print("Select which parameter to change:")
            selections[0] = 1
            print("1) Angle")
            print("2) Number of array elements")
            print("3) Element spacing multiplier")
            print("4) Antenna frequency")
            opt = input("Please input your choice: ")
            if opt == "1":
                selections[1] = input("Enter the angle in degrees: ")
                if selections[1] < 0 or  selections[1] > 180:
                    print("Wrong input, please enter an angle between 0 and 180 ")
                    selections[1] = 0;
            elif opt == "2":
                selections[2] = input("Enter number of array elements: ")
                if selections[2] < 0 or  selections[2] > 5:
                    print("Wrong input, please enter a number between 0 and 5 ")
                    selections[2] = 0;
            elif opt == "3":
                selections[3] = input("Enter spacing multiplier: ")
                if selections[3] < 0 or  selections[3] > 3:
                    print("Wrong input, please enter a multiplier between 0 and 3 ")
                    selections[3] = 0;
            elif opt == "4":
                selections[4] = input("Enter radiating frequency (in MHz): ")
                if selections[4] < 20 or  selections[4] > 2300:
                    print("Wrong input, please enter a frequency between 20MHz and 3 ")
                    selections[4] = 0;
            print("\n")
            print("Thank you for your selection. Please continue your selection, or press q to quit.")

    elif inp == "2":
        mesPhi, mesTheta, mesH, mesV = mainfun()
        maindef(mesPhi, mesTheta, mesH, mesV, selections)
    elif inp == "3":
        database.trdp();
    elif inp == "4":
        dataproc.threedplot();
