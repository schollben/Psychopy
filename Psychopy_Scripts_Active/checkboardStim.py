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
myWin = visual.Window([1920,1080], monitor=mon, units="pix", screen = 0, color = [0,0,0])
monRefreshRate = myWin.getActualFrameRate(nIdentical=60, nMaxFrames=100,nWarmUpFrames=10, threshold=10)
print(monRefreshRate)

# Stimulus properties
width  = 1920 #currently following the monitor size of ACER (120 degrees wide at 20 cm viewing distance)
height = 1080
grid = 2*96 # set the width of each grid 
subGridNum = 2 #number of subGrid on one side when flickering
numBoard = 4 #number of checkers
numStim = 1000 #number of stimulus
interFlickerDelay = 0.10 #delay time in seconds when flickering, cannot be smaller than 0.014 sec)
duration = 1 #duration time of each stimulus in seconds on monitor
isSpike = False #wheter the TTL will be displayed in vertical spike or not
###
#(0,0) is the bottom left corner of the monitor x goes along the height of the grid and y goes along the width of the grid
###

######initialize#####
subGrid = int(grid / subGridNum)
logArrLen = (numpy.floor(height / grid)) * (numpy.floor(width / grid))
flickTime = numpy.round(interFlickerDelay * monRefreshRate) # delay time flickTime * 1/Refresh rate(HZ) of monitor

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
def colorSubgrid_multiple(arr, grid, subGridNum, mat):
    sg = subGrid
    for n in range(0, len(arr)):
        if (subGridNum % 2 == 0) :
            for i in range(0, subGridNum):
                if ((i-1) % 2 == 0):
                    for j in range(0, subGridNum):
                        if ((j-1) % 2 == 0):
                            for a in range(int(int(arr[n, 0]) + i *sg), int(int(arr[n, 0])+ (i+1) * sg)):
                                for b in range(int(int(arr[n, 1]) + j *sg), int(int(arr[n, 1])+ (j+1) * sg)):
                                    mat[a,b] = 1
                        else : 
                            for a in range(int(int(arr[n, 0]) + i *sg), int(int(arr[n, 0])+ (i+1) * sg)):
                                for b in range(int(int(arr[n, 1]) + j *sg), int(int(arr[n, 1])+ (j+1) * sg)):
                                    mat[a,b] = -1
                else : 
                    for j in range(0, subGridNum):
                        if ((j-1) % 2 == 0):
                            for a in range(int(int(arr[n, 0]) + i *sg), int(int(arr[n, 0])+ (i+1) * sg)):
                                for b in range(int(int(arr[n, 1]) + j *sg), int(int(arr[n, 1])+ (j+1) * sg)):
                                    mat[a,b] = -1
                        else :
                            for a in range(int(int(arr[n, 0]) + i *sg), int(int(arr[n, 0])+ (i+1) * sg)):
                                for b in range(int(int(arr[n, 1]) + j *sg), int(int(arr[n, 1])+ (j+1) * sg)):
                                    mat[a,b] = 1
        else : 
            for i in range(0, subGridNum):
                if ((i-1) % 2 == 0):
                    for j in range(0, subGridNum):
                        if ((j-1) % 2 == 0):
                            for a in range(int(int(arr[n, 0]) + (i-1)*sg), int(int(arr[n, 0])+ i * sg)):
                                for b in range(int(int(arr[n, 1]) + (j-1)*sg), int(int(arr[n, 1])+ j * sg)):
                                    mat[a,b] = -1
                        else : 
                            for a in range(int(int(arr[n, 0]) + (i-1)*sg), int(int(arr[n, 0])+ i * sg)):
                                for b in range(int(int(arr[n, 1]) + (j-1)*sg), int(int(arr[n, 1])+ j * sg)):
                                    mat[a,b] = 1
                else : 
                    for j in range(0, subGridNum):
                        if ((j-1) % 2 == 0):
                            for a in range(int(int(arr[n, 0]) + (i-1)*sg), int(int(arr[n, 0])+ i * sg)):
                                for b in range(int(int(arr[n, 1]) + (j-1)*sg), int(int(arr[n, 1])+ j * sg)):
                                    mat[a,b] = 1
                        else : 
                            for a in range(int(int(arr[n, 0]) + (i-1)*sg), int(int(arr[n, 0])+ i * sg)):
                                for b in range(int(int(arr[n, 1]) + (j-1)*sg), int(int(arr[n, 1])+ j * sg)):
                                    mat[a,b] = -1


#Generate all possible configuration
def getConfigArr(checkerNum, leng) :
    configArr = numpy.zeros((numStim, int(leng)), dtype = int)
    seed = 1
    ifValid = False
    for i in range(0,numStim):
        random.seed(seed)
        for j in range(checkerNum):
            while not ifValid :
                r = random.random() * int(leng)
                r = (r - r % 1)
                if configArr[i, int(r)] == 0 :
                    configArr[i, int(r)] = 1
                    break
                else :
                    ifValid = False
        seed = seed + checkerNum
    return configArr
    
#Decode the binary sequence back to coordinate
def decode(config_str, width, gridSize, checkerNum) :
    checkerArr = numpy.zeros((int(checkerNum), 2))
    ind = 0
    col = width / gridSize
    for i in range(0, len(config_str)) :
        if (config_str[i] >= '1') :
            y = (i % col)
            x = (i - y) * grid / col
            y = y * grid
            checkerArr[ind, 0] = x 
            checkerArr[ind, 1] = y
            ind = ind + 1
    return checkerArr

####run#####
decodedArr = []
configArr = getConfigArr(numBoard, int(logArrLen))

for num in range(0, numStim):
    os.chdir(fileAddress)
    c = configArr[num, 0]
    for index in range(1, int(logArrLen)) :
        c = str(c) + str(configArr[num, index])
    x = [c]
    decodedArr = numpy.append(decodedArr, x, axis = 0)

clock = core.Clock();

#baseline
clock.reset();
while clock.getTime() < 5:
    myWin.flip()
    
for num in range(0, numStim):
    
    
    config = str(decodedArr[num])
    locArr = decode(config, width, grid, numBoard)

    print('Stim ' + str(num) + ':' + config)

    # Setting location for one subgrid
    colorSubgrid_multiple(locArr, grid, subGridNum, noise_matrix)
    noiseStim.setImage(noise_matrix)
    
    if isSpike:
        ser.setRTS(True) #stimulus trigger ON
        ser.setRTS(False) #stimulus trigger OFF
    else:
        ser.setRTS(True) #stimulus trigger ON

    #Logging
    file = open(fileName, "a")
    file.write(str(config))
    file.write('\n')
    file.close()

    #Flickering
    clock.reset()

    while clock.getTime() < duration:
        noiseStim.contrast = 1
        rn = clock.getTime()
        while clock.getTime() - rn < interFlickerDelay and clock.getTime() <= duration:
            myWin.flip()
        noiseStim.contrast = -1
        rn = clock.getTime()
        while clock.getTime() - rn < interFlickerDelay and clock.getTime() <= duration:
            myWin.flip()
    noiseStim.contrast = 0
    myWin.flip()
    myWin.flip()
    
    ser.setRTS(False) #stimulus trigger OFF
    
    noise_matrix = 0 * numpy.ones((height, width))

#print file name and address
print('subgrid size : ' + str(subGrid) + ' , grid size : ' + str(grid))
print(fileAddress + fileName)