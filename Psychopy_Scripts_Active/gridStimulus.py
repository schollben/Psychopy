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
grid = 240 # set the width of each grid(ideal if set it as a  common divisor of both width and height)
subGridNum = 2 #number of subGrid on one side when flickering
numBoard = 3 #number of checker board(subGrid)
numStim = 5 #number of stimulus
interFlickerDelay = 0.1 #delay time in seconds when flickering, cannot be smaller than 0.014 sec)
duration = 0.5 #duration time of each stimulus in seconds on monitor
isSpike = True #wheter the TTL will be displayed in vertical spike or not
startSeed = 1000 #seed number to start from
#(0,0) is the bottom left corner of the monitor
#x goes along the height of the grid and y goes along the width of the grid


######initialize#####
subGrid = int(grid / subGridNum)
logArrLen = (numpy.floor(height / grid)) * (numpy.floor(width / grid))
flickTime = numpy.round(interFlickerDelay * monRefreshRate) # delay time flickTime * 1/Refresh rate(HZ) of monitor

logArray = numpy.zeros((int(logArrLen),), dtype=int)
noise_matrix = 0 * numpy.ones((height, width))

noiseStim = visual.ImageStim(myWin, image = noise_matrix, size = (width, height))
noiseStim.setAutoDraw(True)

#USB serial device to time stimulus onset - NOTE this also acts as a TRIGGER for acquistion 
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)

####log#####
fileAddress, fileName = logFunction.logFileNameGeneratorAlt()

#logging the whole script
logScript(os.getcwd(),os.path.basename(__file__), fileAddress, fileName)

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

#Randomly set the location of bottom left corner of the grid
def setXY(width, height, grid, matrix, seed):
    maxX = (numpy.floor(height / grid) - 1) * grid
    maxY = (numpy.floor(width / grid) - 1) * grid
    x = -1
    y = -1
    ifValid = False
    while (not ifValid) : 
        random.seed(seed)
        randomX = random.random()
        randomY = random.random()
        yInGrid = (randomX * width / grid)
        xInGrid = (randomY * height / grid)
        y = (yInGrid - yInGrid % 1) * grid
        x = (xInGrid  - xInGrid  % 1) * grid
        ifValid = ((x <= maxX) and (y <= maxY) and (x >= 0) and (y >= 0))
        if (not (matrix[int(x), int(y)] == 0)) :
            ifValid = False
        seed = seed + 1
    return x, y

#Generate sequence of location for checkerboard 
#    -> index 0 starts from top right corner and increments towards right direction
def generateLog(x, y, gridSize, width, arr) :
    col = width / gridSize
    #row = height / gridSize
    ind = (x/grid) * col + (y/grid)
    arr[int(ind)] = 1
    return arr
    
def getConfigArr (width, height, gridSize, subGridNum, checkerNum, seed) :
    return 0


####run#####
for na in range(0, numStim):
    os.chdir(fileAddress)
    for n in range(0, numBoard):
        stiX, stiY = setXY(width, height, grid, noise_matrix, startSeed)    # Setting location for one subgrid
        print('Grid '+ str(n) + ' : ' + str(stiX)+ ' high and ' + str(stiY) +  
        ' right from the bottom right corner')
        startSeed = startSeed + 1
        colorSubgrid(stiX, stiY, grid, subGridNum, noise_matrix)
        noise_matrix = noise_matrix.reshape((height, width))
        logArray = generateLog(stiX, stiY, grid, width, logArray)
        
        noiseStim.setImage(noise_matrix)
        
        if isSpike:
            ser.setRTS(True) #stimulus trigger ON
            ser.setRTS(False) #stimulus trigger OFF
        else :
            ser.setRTS(True) #stimulus trigger ON
    
    #Logging
    file = open(fileName, "a")
    for i in range(0, int(logArrLen)) :
        file.write(str(logArray[i]))
    file.write('\n')
    file.close()

    #Flickering
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

    ser.setRTS(False) #stimulus trigger OFF
    
    noise_matrix = 0 * numpy.ones((height, width))
    logArray = numpy.zeros((int(logArrLen),), dtype=int)


#print file name and address
print('subgrid size : ' + str(subGrid) + ' , grid size : ' + str(grid))
print(fileAddress + fileName)