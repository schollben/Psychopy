from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp, io
import numpy.matlib
import sys
import os
import serial
from pathlib import Path
import logFunction
from logFunction import logFileNameGenerator, logScript

######setup#####
mon = monitors.Monitor('ACER')
myWin = visual.Window([1920,1080], monitor=mon, units="pix", screen = 1, color = [0,0,0])
monRefreshRate = 75 #refersh rate of mon in Hz

# Stimulus properties
width  = 1920 #currently following the monitor size of ACER
height = 1080
grid = 120 # set the width of each grid(ideal if set it as a  common divisor of both width and height)
delay = 1 #delay time in seconds when flickering, cannot be smaller than 0.014 sec)
duration = 2 #duration time in seconds on monitor
isSpike = True #wheter the TTL will be displayed in vertical spike or not
num = 4 # number of stimulus
startSeed = 1 # seed number to start

######initialize#####
noise_matrix = 0 * numpy.ones((height, width))
flickTime = delay * monRefreshRate # delay time flickTime * 1/Refresh rate(HZ) of monitor
#(0,0) is the bottom left corner of the monitor
#x goes along the height of the grid and y goes along the width of the grid

#USB serial device to time stimulus onset - NOTE this also acts as a TRIGGER for acquistion 
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)

####log#####
stimarray = noise_matrix
fileAddress, fileName = logFunction.logFileNameGenerator(stimarray)
print(fileAddress + fileName)

#logging the whole script
logScript(os.getcwd(),os.path.basename(__file__), fileAddress, fileName)

#Functions
#color the subgrid in black and white    

def colorBoard(grid, mat, seed) :
    random.seed(seed)
    x = int(height/grid)
    y = int(width/grid)
    for i in range(0, x) :
        for j in range(0,y):
            r = random.random()
            if r >= 0.5 :
                for a in range(0, grid):
                    for b in range (0, grid):
                        mat[i * grid + a, j * grid + b] = 1
            else :
                for a in range(0, grid):
                    for b in range (0, grid):
                        mat[i * grid + a, j * grid + b] = -1

####run#####
print('grid size : ' + str(grid))
print(str(int(height/grid)) + ' grids in vetical and '+ str(int(width/grid)) + ' grids in horizontal')

for n in range(0, num):
    colorBoard(grid, noise_matrix, startSeed)
    startSeed = startSeed + 1
    
    stimarray = numpy.append(stimarray, noise_matrix, axis=0)
    numpy.savetxt(fileAddress+fileName,stimarray,fmt="%2d") #updating and overwting file ->  SAVE FOR LATER
    
    noiseStim = visual.ImageStim(myWin, image = noise_matrix, size = (width, height))
    noiseStim.setAutoDraw(True)

    if isSpike:
        ser.setRTS(True) #stimulus trigger ON
        ser.setRTS(False) #stimulus trigger OFF
    else :
        ser.setRTS(True) #stimulus trigger ON

    for i in range(0, int(duration) * monRefreshRate):
        myWin.flip()
    
    ser.setRTS(False) #stimulus trigger OFF

