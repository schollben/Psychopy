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
contrasts  = [4,8,16,32,64]
numContrasts = len(contrasts)
isRandom = 1
numTrials= 2 #Run all the stims this many times
doBlank = 0 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDur = .1
isi = 0.05

#grating parameters
temporalFreq = 4
spatialFreq = 0.08
textureType = 'sqr' #options: 'sqr' = square wave, 'sin' = sinusoidal
stimSize = 250 #deg

######initialize#####
#USB serial device to time stimulus onset - NOTE this also acts as a TRIGGER for acquistion 
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)

mon = monitors.Monitor('Acer') # mon.setGamma(1.6)?
myWin = visual.Window([1920,1080],monitor=mon, units="deg",screen = 1)

myWin.gamma = 1.6 #human calibrated with gammaMotionNull - only works in duplication display mode?????

#logging
stimarray = numpy.empty((0,3), int) #[stimulus number, orientation, contrast]
fileAddress, fileName = logFunction.logFileNameGenerator(stimarray)
print(fileAddress + fileName)

#logging the whole script
logScript(os.getcwd(),os.path.basename(__file__), fileAddress, fileName)

#create grating stims
gratingStim = visual.GratingStim(win=myWin, mask='circle', tex=textureType ,units='deg',
    pos=[0, 0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim.setAutoDraw(True)

#create stimulus combinations and order
totalNumStim = len(orientations)*len(contrasts)+doBlank
stimOrder = numpy.arange(0,totalNumStim)

if doBlank:
    stimOrder.append(blankID)
    totalNumStim = totalNumStim + 1
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
while clock.getTime() < 5:
    myWin.flip()


#stimulus presentation
for trial in range(0,numTrials): 
    
    if isRandom:
        random.shuffle(stimOrder)
    
    print("Beginning Trial",trial+1)
    
    for stimNumber in stimOrder:
        print(stimNumber)

        if stimNumber == len(orientations):
            print("blank")
            gratingStim.setContrast(0)
            print("\tStim",stimNumber+1," (blank)")  #display stim
        else:
            gratingStim.setContrast( contrasts[stimNumber] / 100 )
            gratingStim.ori = orientations[stimNumber]-90 # convert orientations to standard lab notation
            print("\tStim",stimNumber+1,orientations[stimNumber],' deg ',contrasts[stimNumber],' %')  #display stim
        
        clock.reset()
        ser.setRTS(True) #stimulus trigger ON
        while clock.getTime() < stimDur:
            gratingStim.setPhase(0 + clock.getTime()*temporalFreq)
            myWin.flip()
        ser.setRTS(False) #stimulus trigger OFF
        
        #logging
        stimarray = numpy.append( stimarray, numpy.array([[stimNumber+1, orientations[stimNumber], contrasts[stimNumber]]]), axis=0)
        numpy.savetxt(fileAddress+fileName,stimarray,fmt="%4d") #updating and overwting file
        
        #now do ISI
        if isi !=0:
            gratingStim.setContrast(0)
            clock.reset()
            while clock.getTime() < isi:
                myWin.flip()


