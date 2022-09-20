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
numCells = 2 #always include 2 cells with the first ROI being a SHAM location?
numTrials= 1

numOrientations = 4
orientations = numpy.arange(0,360,360.0/numOrientations)
contrasts  = [16,64]
numContrasts = len(contrasts)
isRandom = 1
##### ASSUMING 120Hz frame rate!

#grating parameters
temporalFreq = 4
spatialFreq = 0.08
textureType = 'sqr' #options: 'sqr' = square wave, 'sin' = sinusoidal
stimSize = 300 #deg

######initialize#####
#USB serial devices to time stimulus onset
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)
#deviceName2 = "COM4"
#ser2 = serial.Serial(deviceName2, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
#ser2.setRTS(False)
#ser2.setDTR(False)

mon = monitors.Monitor('ACER')
myWin = visual.Window([1920,1080],monitor=mon, units="deg",screen = 0)
thisGamma = 1.6 #human calibrated with gammaMotionNull - only works in duplication display mode?

#logging
stimarray = numpy.empty((0,5), int) 
fileAddress, fileName = logFunction.logFileNameGenerator(stimarray)
print(fileAddress + fileName)

#logging the whole script
logScript(os.getcwd(),os.path.basename(__file__), fileAddress, fileName)

#create grating stims
gratingStim = visual.GratingStim(win=myWin, mask='circle', tex=textureType ,units='deg',
    pos=[0, 0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim.setAutoDraw(True)

#create stimulus combinations and order
totalNumStim = len(orientations)*len(contrasts)
#repeat parameters for combinations
contrasts = numpy.repeat(contrasts,numOrientations,axis=0)
orientations = numpy.tile(orientations,numContrasts)

####run#####

print('n = '+str(totalNumStim)+' stims will be run for '+str(numTrials)+' trials')

#gray screen
gratingStim.setContrast(0)

#delay and trigger to start imaging acquisition
clock = core.Clock();
clock.reset()
while clock.getTime() < 10:
    myWin.flip()

#stimulus presentation
for trial in range(0,numTrials):
        
    stimOrder = numpy.arange(0,totalNumStim)
    stimOrder = numpy.repeat(stimOrder,numCells) #rep stimOrder for each cell
    if isRandom:
        random.shuffle(stimOrder)  #randomize each trial
    stimOrder = stimOrder.reshape(numCells,totalNumStim) #create 2D array
        
    for k in range(0,totalNumStim):
        
        for ncell in range(0,numCells):
            
            stimNumber = stimOrder[ncell,k]
            
            gratingStim.setContrast(0)
            for frmn in range(0, 60):
                myWin.flip()
                
            gratingStim.setContrast( contrasts[stimNumber] / 100 )
            gratingStim.ori = orientations[stimNumber]-90 # convert orientations to standard lab notation
            print("\tStim",stimNumber+1,'cell: ',ncell+1,'  ',orientations[stimNumber],' deg ',contrasts[stimNumber],' %')  #display stim
            
                
            ser.setRTS(True) #stimulus trigger ON
            for frmn in range(0, 120): #frame rate = 120 Hz
                gratingStim.setPhase(0.05, '+')
                myWin.flip()
                if frmn == 12:
                    ser.setDTR(True) #photostim trigger ON (100ms TTL pulse)
                if frmn == 14:
                    ser.setDTR(False) #photostim trigger OFF
            ser.setRTS(False) #stimulus trigger OFF
            ser.setDTR(False) #photostim trigger OFF
            
            #logging
            temparray = numpy.array([[ncell+1, trial+1, stimNumber+1, orientations[stimNumber], contrasts[stimNumber]]])
            stimarray = numpy.append( stimarray, temparray, axis=0)
            numpy.savetxt(fileAddress+fileName,stimarray,fmt="%4d") #updating and overwting file
        



