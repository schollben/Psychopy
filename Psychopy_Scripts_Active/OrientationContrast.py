from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import numpy.matlib
import sys
import os
import serial
from pathlib import Path


######setup#####
numOrientations = 8
orientations = numpy.arange(0,360,360.0/numOrientations)
contrasts  = [4,8,16,32,64]
#contrasts  = [6.25,12.5,25,50,100]
numContrasts = len(contrasts)
isRandom = 0
numTrials= 1 #Run all the stims this many times
doBlank = 0 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDur = 2
isi = 1

#grating parameters
temporalFreq = 4
spatialFreq = 0.1
textureType = 'sqr' #options: 'sqr' = square wave, 'sin' = sinusoidal
stimSize = 120 #deg

######initialize#####
#USB serial device to time stimulus onset
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False) #used to trig stimulus onset/offset
ser.setDTR(False) #used to trig START and photostim

mon = monitors.Monitor('ACER')
myWin = visual.Window([1920,1080],monitor=mon, units="deg",screen = 0)

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
FileName = '_'+time.strftime("%H%M")+'_'+FileName    
print(logFilePath+FileName) #new file name and location
stimarray = numpy.empty((0,3), int) #[stimulus number, orientation, contrast]
numpy.savetxt(logFilePath+FileName,stimarray)

#create grating stims
gratingStim = visual.GratingStim(win=myWin, mask='circle', tex=textureType ,units='deg',
    pos=[0, 0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim.setAutoDraw(True)

#grayStim = visual.GratingStim(win=myWin,units='deg',
#    pos=[0, 0],size=[134,134], contrast=0, autoLog=False)
#grayStim.setAutoDraw(True)

#create stimulus combinations and order
totalNumStim = len(orientations)*len(contrasts)+doBlank
stimOrder = numpy.arange(0,totalNumStim)

if isRandom:
    random.shuffle(stimOrder)
#repeat parameters for combinations
contrasts = numpy.repeat(contrasts,numOrientations,axis=0)
orientations = numpy.tile(orientations,numContrasts)

####run#####

#gray screen
gratingStim.setContrast(0)

#delay
clock = core.Clock();
clock.reset()
while clock.getTime() < 1:
    myWin.flip()

#start trigger 
ser.setDTR(True)
myWin.flip()
ser.setDTR(False)

#stimulus presentation
for trial in range(0,numTrials): 
    
    print("Beginning Trial",trial+1)
    
    for stimNumber in stimOrder:

        if stimNumber == len(orientations):
            gratingStim.setContrast(0)
            print("\tStim",stimNumber+1," (blank)")  #display stim
        else:
            gratingStim.setContrast( contrasts[stimNumber] / 100 )
            gratingStim.ori = orientations[stimNumber]-90 # convert orientations to standard lab notation
            print("\tStim",stimNumber+1,orientations[stimNumber],' deg ',contrasts[stimNumber],' %')  #display stim
        
        
        clock.reset
        
        ser.setRTS(True) #stimulus trigger ON

        while clock.getTime() < stimDur+1:
            gratingStim.setPhase(0 + clock.getTime()*temporalFreq)
            myWin.flip()
            
        ser.setRTS(False) #stimulus trigger OFF
        
        #logging
        stimarray = numpy.append( stimarray, numpy.array([[stimNumber, orientations[stimNumber], contrasts[stimNumber]]]), axis=0)
        numpy.savetxt(logFilePath+FileName,stimarray,fmt="%4d") #updating and overwting file
        
        #now do ISI
        if isi !=0:
            gratingStim.setContrast(0)
            clock.reset()
            while clock.getTime() < isi:
                myWin.flip()
                
        if event.getKeys(keyList = ['escape'], modifiers=False, timeStamped=False):
            break
        event.clearEvents()            

frame_rate = myWin.getActualFrameRate(nIdentical=60, nMaxFrames=100,nWarmUpFrames=10, threshold=10)
print(frame_rate)




