from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import numpy.matlib
import sys
import os
import serial
from pathlib import Path


######setup#####
numCells = 2
numTrials= 1 

numOrientations = 4
orientations = numpy.arange(0,360,360.0/numOrientations)
contrasts  = [16,64]
numContrasts = len(contrasts)
isRandom = 1
doBlank = 0 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDur = 1.0
isi = 0.5

#grating parameters
temporalFreq = 8
spatialFreq = 0.10
textureType = 'sqr' #options: 'sqr' = square wave, 'sin' = sinusoidal
stimSize = 100 #deg

######initialize#####
#USB serial device to time stimulus onset
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)

mon = monitors.Monitor('ACER')
myWin = visual.Window([1920,1080],monitor=mon, units="deg",screen = 1)
thisGamma = 1.6 #human calibrated with gammaMotionNull - only works in duplication display mode?
myWin.gamma = [thisGamma, thisGamma, thisGamma]

#logging
dataPath='D:\\Pyschopy\\'
date = (time.strftime("%Y-%m-%d"))
directory = dataPath+date
if not os.path.exists(directory):
    os.mkdir(directory)
logFilePath =dataPath+date+'\\'+Path(__file__).stem #filepath
i = 0
FileName = f"{i:03}"+'.txt'
while os.path.exists(logFilePath+FileName):
    i = i+1
    FileName = f"{i:03}"+'.txt'
print(logFilePath+FileName) #new file name and location
#[cell number, trial number, stimulus number, orientation, contrast]
stimarray = numpy.empty((0,5), int) 
numpy.savetxt(logFilePath+FileName,stimarray)

#create grating stims
gratingStim = visual.GratingStim(win=myWin, mask='circle', tex=textureType ,units='deg',
    pos=[0, 0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim.setAutoDraw(True)

#create stimulus combinations and order
totalNumStim = len(orientations)*len(contrasts)+doBlank
stimOrder = numpy.arange(0,totalNumStim)
print(stimOrder) 
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

#delay
clock = core.Clock();
clock.reset()
while clock.getTime() < 1:
    myWin.flip()

#stimulus presentation
for trial in range(0,numTrials): 
    
    if isRandom:
        random.shuffle(stimOrder)  #randomize each trial
        
    for ncell in range(0,numCells):
        
        for stimNumber in stimOrder:
            
            #start block - current length is 1.5 sec (~45 frames)
            ser.setRTS(True) #start acquisition trigger
            myWin.flip()
            ser.setRTS(False) #start acquisition trigger

            
            if isi !=0:
                gratingStim.setContrast(0)
                clock.reset()
                while clock.getTime() < isi:
                    myWin.flip()
                    
            if stimNumber == len(orientations):
                gratingStim.setContrast(0)
                print("\tStim",stimNumber+1," (blank)")  #display stim
            else:
                gratingStim.setContrast( contrasts[stimNumber] / 100 )
                gratingStim.ori = orientations[stimNumber]-90 # convert orientations to standard lab notation
                print("\tStim",stimNumber+1,orientations[stimNumber],' deg ',contrasts[stimNumber],' %')  #display stim
            
            ser.setRTS(True) #stimulus trigger ON
            for frmn in range(0, (60 - 1) * stimDur ): #frame rate = 60 Hz
                gratingStim.setPhase(0.05, '+')
                myWin.flip()
                if frmn == 6:
                    ser.setDTR(True) #photostim trigger ON
                if frmn == 15:
                    ser.setDTR(False) #photostim trigger OFF
            ser.setRTS(False) #stimulus trigger OFF
            ser.setDTR(False) #photostim trigger OFF
            
            #logging
            temparray = numpy.array([[ncell+1, trial+1, stimNumber+1, orientations[stimNumber], contrasts[stimNumber]]])
            stimarray = numpy.append( stimarray, temparray, axis=0)
            numpy.savetxt(logFilePath+FileName,stimarray,fmt="%4d") #updating and overwting file
        






