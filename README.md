# Cell Tower Signal Diagnostic Drone (CTSDD) - Senior Design

  # Project Summary
    The process of diagnosing and repairing incorrect cell tower sector antennas can often be time-consuming and dangerous to human
    lives. The Cell Tower Signal Diagnostic Drone (CTSDD) seeks to mitigate both of these issues by using an autonomous flight path and
    software defined radio to gather antenna data that is used to generate the antenna's radiation pattern. The system then compares the
    measured radiation pattern to the ideal radiation pattern of the antenna and uses a diagnostic database to give a recommendation to
    the customer on how to correct the cell tower's signal issue.

  # Breakdown of Sub-Systems
    Autonomous Flight - Blake Thompson:
      Generates and executes an autonomous flight path 
      Python script utilizing the Dronekit library 
      Serial connection between a Raspberry Pi 3 Model B and a Pixhawk 1
      Operates a custom-built hexacopter 
      The operator may change to manual control at any time during autonomous flight, should the situation require it
      
    Data Transfer Management - Josh Suen:
      Utilizes Python to connect the Raspberry Pi to all drone peripherals
      Tested the SDR to ensure accurate results
      Collaborated with the Data Processing and Mapping Subsystem to determine an appropriate save format
      Automated data collection
      Created rudimentary user interface with error catching
      
    Data Processing & Mapping - Ron Hadri:
      Parses magnitude and coordinate data
      Calculates percent error between measurements of a point
      Filters data to include relevant gain values
      Interpolates points
      Plots radiation patterns

    Diagnostic Database - Gerardo Montemayor:
      Simulate and 3D plot of antenna array 
      Allows user to modify antenna array simulation
      Compare theoretical and measured data
      Measure percentage error and track the horizontal and vertical patterns from theoretical and measured data
      Display electrical antenna characteristics, and suggest user fixes to increase performance 
      Allow user to control system through master file interface

  # Getting Started
    Prerequisites
      1) Install an IDE to run python 3.0
      2) Go to ECEN403-404-CTSDD > Blake_Thompson and open up the most recent coordData_mmddyy file
      3) Save the most recent coordData_mmddyy file to your computer
      4) Go to ECEN403-404-CTSDD > JoshuaSuen and open up the corresponding magData_mmddyy and freqData_mmddyy files
      5) Save the corresponding magData_mmddyy and freqData_mmddyy files to your computer
      
    Processing the Data
      1) Go to ECEN403-404-CTSDD > Ron Hadri > DataProcMap_040119.py and save it to your computer
      2) Open DataProcMap usig the IDE you have installed for python
      3) Under the "I/O" category in the DataProcMap_040119.py code, ensure that the correct files are being read
      4) Under the "Variables" category in the DataProcMap_040119.py code, ensure that the freqRange is below 1.5 to filter out undesired
         frequencies
      5) Run the program to view the Average Perect Error of the system, Frequency vs Gain plot, and the radiation plots of the data
      
    Using the Diagnostic Database
      1) Go to ECEN403-404-CTSDD > Gerardo Montemayor > database.py and save it to your computer
      2) Go to ECEN403-404-CTSDD > Gerardo Montemayor > dataproc.py and save it to your computer
      3) Go to ECEN403-404-CTSDD > Gerardo Montemayor > gui.py and save it to your computer
      4) If the dataproc.py from the previous subsystem is present in the folder, either overwrite or delete the old one
      5) Open database.py, dataproc.py, gui.py usig the IDE you have installed for python
      6) Under the "I/O" category in the dataproc.py code, ensure that the correct files are being read
      7) Under the "Variables" category in the dataproc.py code, ensure that the freqRange is below 1.5 to filter out undesired
         frequencies
      8) Run the program and select your desired options via the command line interface (CLI) that is displayed to view the Average              Percent Error of the system, Frequency vs Gain plot, the radiation plots of the data, the 3D theoretical radiation plot, side            lobe tracking, and the percent error plot between the measured and theoretical data
