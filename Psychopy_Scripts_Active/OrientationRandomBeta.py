from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import numpy.matlib
import sys
import os
import serial
from pathlib import Path
import randomgenerator.randomgenerator as gener
import logFunction
from logFunction import logFileNameGenerator


######setup#####
isRandom = True
numTrials= 1 #Run all the stims this many times
doBlank = False #False for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDur = 2
isi = 1
setPhase = True #If not setting randomly selected phase, set it False
logPrefix = 'randomOrientation' #set the prefix of log file

#grating parameters
temporalFreq = 8
#spatialFreq = 0.5
textureType = 'sqr' #options: 'sqr' = square wave, 'sin' = sinusoidal
stimSize = 10 #deg

######initialize#####
#USB serial device to time stimulus onset
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1) #RTS: stimulus onset trigger     DTS: other
ser.setRTS(False)
ser.setDTR(False)

mon = monitors.Monitor('ACER')
myWin = visual.Window([1920,1080],monitor=mon, units="deg",screen = 1)

#logging
'''
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
stimarray = numpy.empty((0,6), int) #[stimulus number, orientation, contrast]
numpy.savetxt(logFilePath+FileName,stimarray)'''
stimarray = numpy.empty((0,6), int) #[stimulus number, orientation, contrast]
fileAddress, fileName = logFunction.logFileNameGenerator(logPrefix)
print(fileAddress)
print(fileName)

#create grating stims
gratingStim = visual.GratingStim(win=myWin, mask='gauss', tex=textureType ,units='deg',
    pos=[0, 0], size=stimSize, autoLog=False)
gratingStim.setAutoDraw(True)

#grayStim = visual.GratingStim(win=myWin,units='deg',
#    pos=[0, 0],size=[134,134], contrast=0, autoLog=False)
#grayStim.setAutoDraw(True)

#create stimulus combinations and order
totalNumStim = 5 #set the total number of iteration
stimOrder = numpy.arange(0,totalNumStim)
print(totalNumStim) 
if isRandom:
    random.shuffle(stimOrder)
if doBlank:
    stimOrder.append(blankID)
    totalNumStim = totalNumStim + 1

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
    
    print("Beginning Trial",trial+1)
    
    for stimNumber in range(0, totalNumStim):
        cont, size, freq, ornt, phase = gener.randomgenerator()
        
        if doBlank and stimNumber == len(numpy.arange(0,360,360.0/8)):
            gratingStim.setContrast(0)
            print("\tStim",stimNumber+1," (blank)")  #display stim
        else:
            gratingStim.setContrast( cont )
            gratingStim.setOri(numpy.rad2deg(ornt)) # convert orientations to standard lab notation
            gratingStim.setSF(freq)
            gratingStim.setSize(size)
            
            if setPhase: 
                gratingStim.setPhase(phase)
            
            print("\tStim",stimNumber+1,numpy.rad2deg(ornt),' deg ',str(cont * 100),' %', 
            ' sf ',freq,  ' size ',size,  ' phase ',phase)  #display stim
        
        clock.reset
        ser.setRTS(True) #stimulus trigger ON
        while clock.getTime() < stimDur:
            gratingStim.setPhase(0 + clock.getTime()*temporalFreq)
            myWin.flip()
        ser.setRTS(False) #stimulus trigger OFF
        
        #logging
        stimarray = numpy.append( stimarray, numpy.array([[stimNumber, numpy.rad2deg(ornt), cont, freq, size, phase]]), axis=0)
        numpy.savetxt(fileAddress+fileName,stimarray,fmt= ["%4d","%1.3f", "%1.3f", "%1.3f", "%1.3f", "%1.3f"])
        
        #now do ISI
        if isi !=0:
            gratingStim.setContrast(0)
            clock.reset()
            while clock.getTime() < isi:
                myWin.flip()





