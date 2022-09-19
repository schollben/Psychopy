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
numOrientations = 8
orientations = numpy.arange(0,360,360.0/numOrientations)
gratsizes = [10,20,40,80,160] #radius in deg
contrasts  = [99] #[4,8,16,32,64]

isRandom = 0
numTrials= 1 #Run all the stims this many times
doBlank = 0 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDur = 0.5
isi = 0.5

#grating parameters
temporalFreq = 4
spatialFreq = 0.1
textureType = 'sqr' #options: 'sqr' = square wave, 'sin' = sinusoidal
stimSize = 250 #deg

######initialize#####
#USB serial device to time stimulus onset - NOTE this also acts as a TRIGGER for acquistion 
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)

mon = monitors.Monitor('Acer') # mon.setGamma(1.6)?
myWin = visual.Window([1920,1080],monitor=mon, units="deg",screen = 0)

myWin.gamma = 1.6 #human calibrated with gammaMotionNull - only works in duplication display mode?????

#logging
stimarray = numpy.empty((0,3), int) #[stimulus number, orientation, contrast, sitim size]
fileAddress, fileName = logFunction.logFileNameGenerator(stimarray)
print(fileAddress + fileName)

#logging the whole script
logScript(os.getcwd(),os.path.basename(__file__), fileAddress, fileName)

#annulus setup
radius = filters.makeRadialMatrix(256)
#note - creating some space in between annuli (its not 0.5)
annulus = numpy.where(radius< 1, 1, 0) * numpy.where(radius> 0.55, 1, 0) * 2 - 1

#create grating stims
gratingStim = visual.GratingStim(win=myWin, mask=annulus, tex=textureType ,units='deg',
    pos=[0, 0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim.setAutoDraw(True)

#create mask
#maskStim = visual.Circle(win=myWin, units='deg',pos=[0,0])
#maskStim.setContrast(0);
#maskStim.setAutoDraw(True)
#maskStim.size = 5

#create stimulus combinations and order
numContrasts = len(contrasts)
numSizes = len(gratsizes)
totalNumStim = 1*numContrasts*numSizes+doBlank
stimOrder = numpy.arange(0,totalNumStim)

if isRandom:
    random.shuffle(stimOrder)
if doBlank:
    stimOrder.append(blankID)
    totalNumStim = totalNumStim + 1
#repeat parameters for combinations
contrasts = numpy.repeat(contrasts,1*numSizes,axis=0)
gratsizes = numpy.repeat(gratsizes,1,axis=0)
gratsizes = numpy.tile(gratsizes,numContrasts)
#orientations = numpy.tile(orientations,numContrasts*numSizes)

####run#####

print('n = '+str(totalNumStim)+' stims will be run for '+str(numTrials)+' trials')

#gray screen
gratingStim.setContrast(0)

#delay and trigger to start imaging acquisition
clock = core.Clock();
clock.reset()
while clock.getTime() < 5:
    myWin.flip()

#stimulus presentation
for trial in range(0,numTrials): 
    
    print("Beginning Trial",trial+1)
    
    for stimNumber in stimOrder:
        print(stimNumber)
        
        gratingStim.size = gratsizes[stimNumber]
        gratingStim.setContrast( contrasts[stimNumber] / 100 )
        print("\tStim",stimNumber+1,contrasts[stimNumber],' %',gratsizes[stimNumber],' deg')  #display stim
    
        for n in range(0,numOrientations):
            gratingStim.ori = orientations[n]
            clock.reset()
            ser.setRTS(True) #stimulus trigger ON
            while clock.getTime() < stimDur:
                gratingStim.setPhase(0 + clock.getTime()*temporalFreq)
                myWin.flip()
            ser.setRTS(False) #stimulus trigger OFF
        
        #logging
        stimarray = numpy.append( stimarray, numpy.array([[stimNumber+1, contrasts[stimNumber], gratsizes[stimNumber]]]), axis=0)
        numpy.savetxt(fileAddress+fileName,stimarray,fmt="%4d") #updating and overwting file
        
        #now do ISI
        if isi !=0:
            gratingStim.setContrast(0)
            clock.reset()
            while clock.getTime() < isi:
                myWin.flip()


