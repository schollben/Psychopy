from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp, io
import numpy.matlib
import sys
import os
import serial
from pathlib import Path
import logFunction
from logFunction import logFileNameGeneratorAlt, logScript

######setup#####
mon = monitors.Monitor('Acer')
myWin = visual.Window([1920,1080], monitor=mon, units="pix", screen = 1, color = [0,0,0])
monRefreshRate = myWin.getActualFrameRate(nIdentical=60, nMaxFrames=100,nWarmUpFrames=10, threshold=10)

# Stimulus properties
width  = 1920 #currently following the monitor size of ACER
height = 1080
grid = 120 # set the width of each grid(ideal if set it as a  common divisor of both width and height)
duration = 1 #duration time in seconds on monitor, cannot be smaller than 0.014 sec
isSpike = True #wheter the TTL will be displayed in vertical spike or not
num = 10 # number of stimulus
startSeed = 1 # seed number to start
sparseness = 0.9 #in scale from 0 to 1

######initialize#####
noise_matrix = 0 * numpy.ones((height, width))
noiseStim = visual.ImageStim(myWin, image = noise_matrix, size = (width, height))
#(0,0) is the bottom left corner of the monitor
#x goes along the height of the grid and y goes along the width of the grid

#USB serial device to time stimulus onset - NOTE this also acts as a TRIGGER for acquistion 
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)

#get frame rate and calculate number of frames per stimulus
numFrames = numpy.round(int(duration) * monRefreshRate)

####log#####
logArrLen = (numpy.floor(height / grid)) * (numpy.floor(width / grid))
logArray = numpy.zeros((int(logArrLen),), dtype=int)
fileAddress, fileName = logFunction.logFileNameGeneratorAlt()

#logging the whole script
logScript(os.getcwd(),os.path.basename(__file__), fileAddress, fileName)

#Functions    
#color the subgrid in black and white    
def colorBoard(grid, mat, width, height, seed, log, sp) :
    random.seed(seed)
    col = width / grid
    lowerBound = (1-sp)/2
    upperBound = 1-((1-sp)/2)
    x = int(height/grid)
    y = int(width/grid)
    for i in range(0,x) :
        for j in range(0,y):
            r = random.random()
            if r <= lowerBound :
                for a in range(0, grid):
                    for b in range (0, grid):
                        mat[i * grid + a, j * grid + b] = 1
                log[int(i*col+j)] = 1
            elif r >= upperBound:
                for a in range(0, grid):
                    for b in range (0, grid):
                        mat[i * grid + a, j * grid + b] = -1
                log[int(i*col+j)] = -1
            else :
                log[int(i*col+j)] = 0
    return mat, log

####run#####
noiseStim.setAutoDraw(True)

for n in range(0, num):
    m, l = colorBoard(grid, noise_matrix, width, height, startSeed, logArray, sparseness)
    startSeed = startSeed + 1
    noist_matrix = m
    logArray = l;
    
    noise_matrix = noise_matrix.reshape((height, width))
    noiseStim.setImage(noise_matrix)
    
    #Logging
    config = str(logArray[0])
    file = open(fileAddress + fileName, "a")
    for index in range(1, int(logArrLen)) :
        config = str(config) + str(logArray[index])
    file.write(config)
    file.write('\n')
    file.close()
    
    if isSpike:
        ser.setRTS(True) #stimulus trigger ON
        ser.setRTS(False) #stimulus trigger OFF
    else :
        ser.setRTS(True) #stimulus trigger ON
    
    clock = core.Clock();
    clock.reset()
    
    while clock.getTime() < duration:
        myWin.flip()
        
    ser.setRTS(False) #stimulus trigger OFF
    noise_matrix = 0 * numpy.ones((height, width))
    
#print file name and address
print('grid size : ' + str(grid))
print(str(int(height/grid)) + ' grids in vetical and '+ str(int(width/grid)) + ' grids in horizontal')
print(fileAddress + fileName)

