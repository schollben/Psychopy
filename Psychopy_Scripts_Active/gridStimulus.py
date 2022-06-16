from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import numpy.matlib
import sys
import os
import serial
from pathlib import Path
import logFunction
from logFunction import logFileNameGenerator

######setup#####
mon = monitors.Monitor('ACER')
myWin = visual.Window([1920,1080], monitor=mon, units="pix", screen = 1, color = [0,0,0])
monRefreshRate = 75 #refersh rate of mon in Hz
logPrefix = 'randomGrid' #set the prefix of log file

# Stimulus properties
width  = 1920 #currently following the monitor size of ACER
height = 1080
grid = 120 # set the width of each grid(ideal if set it as a  common divisor of both width and height)
subGridNum = 12 #number of subGrid on one side when flickering
num = 1 #number of stimulus
delay = 1 #delay time in seconds when flickering 
duration = 3 #duration time in seconds on monitor
#x goes along the height of the grid and y goes along the width of the grid

######initialize#####
subGrid = int(grid / subGridNum)
noise_matrix = 0 * numpy.ones((height, width))
flickTime = delay * monRefreshRate # delay time flickTime * 1/Refresh rate(HZ) of monitor

#Functions
#color the subgrid in black and white    
def colorSubgrid(x, y, grid, subGridNum, mat):
    sg = subGrid
    if (subGridNum % 2 == 0) :
        for i in range(0, subGridNum):
            if ((i-1) % 2 == 0):
                for j in range(0, subGridNum):
                    if ((j-1) % 2 == 0):
                        for a in range(int(x + i *sg), int(x+ (i+1) * sg)):
                            for b in range(int(y + j *sg), int(y+ (j+1) * sg)):
                                mat[a,b] = 1
                    else : 
                        for a in range(int(x + i *sg), int(x+ (i+1) * sg)):
                            for b in range(int(y + j *sg), int(y+ (j+1) * sg)):
                                mat[a,b] = -1
            else : 
                for j in range(0, subGridNum):
                    if ((j-1) % 2 == 0):
                        for a in range(int(x + i *sg), int(x+ (i+1) * sg)):
                            for b in range(int(y + j *sg), int(y+ (j+1) * sg)):
                                mat[a,b] = -1
                    else :
                        for a in range(int(x + i *sg), int(x+ (i+1) * sg)):
                            for b in range(int(y + j *sg), int(y+ (j+1) * sg)):
                                mat[a,b] = 1
    else : 
        for i in range(0, subGridNum):
            if ((i-1) % 2 == 0):
                for j in range(0, subGridNum):
                    if ((j-1) % 2 == 0):
                        for a in range(int(x + (i-1)*sg), int(x+ i * sg)):
                            for b in range(int(y + (j-1)*sg), int(y+ j * sg)):
                                mat[a,b] = -1
                    else : 
                        for a in range(int(x + (i-1)*sg), int(x+ i * sg)):
                            for b in range(int(y + (j-1)*sg), int(y+ j * sg)):
                                mat[a,b] = 1
            else : 
                for j in range(0, subGridNum):
                    if ((j-1) % 2 == 0):
                        for a in range(int(x + (i-1)*sg), int(x+ i * sg)):
                            for b in range(int(y + (j-1)*sg), int(y+ j * sg)):
                                mat[a,b] = 1
                    else : 
                        for a in range(int(x + (i-1)*sg), int(x+ i * sg)):
                            for b in range(int(y + (j-1)*sg), int(y+ j * sg)):
                                mat[a,b] = -1

#Randomly set the location of bottor right corner of the grid
def setXY(width, height, grid, matrix):
    x = -1
    y = -1
    ifValid = False
    while (not ifValid) : 
        randomX = random.random()
        randomY = random.random()
        y = ((randomX * width / grid) - (randomX * width / grid) % 1) * grid
        x = ((randomY * height / grid) - (randomY * height / grid) % 1) * grid
        ifValid = ((x <= height - grid) and (y <= width - grid) and (x >= 0) and (y >= 0))
        if (not (matrix[int(x), int(y)] == 0)) :
            ifValid = False
    return x, y


####run#####
for n in range(0, num):
    # Setting location for one subgrid
    stiX, stiY = setXY(width, height, grid, noise_matrix)
    print('Grid '+ str(n) + ' : ' + str(stiX)+ ' high and ' + str(stiY) +  
    ' right from the bottom right corner')
    colorSubgrid(stiX, stiY, grid, subGridNum, noise_matrix)
    print('subgrid size : ' + str(subGrid) + ' , grid size : ' + str(grid))
    noise_matrix = noise_matrix.reshape((height, width))
    
    # Use numpy array as ImageStim
    noiseStim = visual.ImageStim(myWin, image = noise_matrix, size = (width, height))
    
#Flickering
noiseStim.setAutoDraw(True)

clock = core.Clock();
clock.reset()

while clock.getTime() < duration:
    noiseStim.contrast = 1
    for i in range(0, int(flickTime)):
        myWin.flip()
        if clock.getTime() >= duration:
            break
    noiseStim.contrast = -1 #invert the color of subgrids
    for i in range(0, int(flickTime)):
        myWin.flip()
        if clock.getTime() >= duration:
            break


####log#####
'''
stimarray = noise_matrix
fileAddress, fileName = logFunction.logFileNameGenerator(logPrefix)
print(fileAddress)
print(fileName)
numpy.savetxt(fileAddress+fileName,stimarray,fmt="%1.1f")'''
    