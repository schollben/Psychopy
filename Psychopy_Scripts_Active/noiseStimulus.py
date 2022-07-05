from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
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
myMouse = event.Mouse(win=myWin)

# Stimulus properties
width  = 1920 #currently following the monitor size of ACER
height = 1080
grid = 120 # set the width of each grid(ideal if set it as a  common divisor of both width and height)
num = 4 #number of sequence of stimulus
color = 'hotpink'
flickTime = 1 #cannot be smaller than 0.014 sec)

######initialize#####
noise_matrix = 0 * numpy.ones((height, width))
isWhite = True
stimarray = numpy.empty((0,2), int)
#(0,0) is the center of the monitor
#x goes along with the width and y goes along with the height

####log#####
fileAddress, fileName = logFunction.logFileNameGenerator(stimarray)
print(fileAddress + fileName)

#logging the whole script
logScript(os.getcwd(),os.path.basename(__file__), fileAddress, fileName)

#Functions            
#randomly set the location of the center of the grid
def setXY(width, height, grid, matrix):
    x = -1
    y = -1
    ifValid = False
    while (not ifValid) : 
        randomX = random.random()
        randomY = random.random()
        x = ((randomX * width / grid) - (randomX * width / grid) % 1) * grid
        y = ((randomY * height / grid) - (randomY * height / grid) % 1) * grid
        ifValid = ((x <= (width - grid)/2) and (y <= (height - grid)/2) and (x >= 0) and (y >= 0))
    signX = random.choice((-1,1))
    signY = random.choice((-1,1))
    x = x * signX
    y = y * signY
    return x, y

#delay
clock = core.Clock();
clock.reset()

while clock.getTime() < 1:
    myWin.flip()
    
####run#####
for n in range(0, num):
    stiX, stiY = setXY(width, height, grid, noise_matrix)
    print('Grid '+ str(n) + ' : ( ' + str(stiX)+ ' , ' + str(stiY) +  ' )')
    stimarray = numpy.append( stimarray, numpy.array([[stiX, stiY]]), axis=0)
    
    ###logging####
    numpy.savetxt(fileAddress+fileName,stimarray,fmt="%1.1f")
    
    noiseStim = visual.rect.Rect(win=myWin, size = (grid, grid))
    noiseStim.setAutoDraw(True)
    
    if isWhite :
        noiseStim.color = 'white'
        noiseStim.pos = (stiX, stiY)
    else : 
        noiseStim.color = str(color)
        noiseStim.pos = (stiX, stiY)
    
    for i in range(0, int(flickTime) * 75):
        myWin.flip()
    
    isWhite = not isWhite
    noiseStim.color = [0,0,0]
    
