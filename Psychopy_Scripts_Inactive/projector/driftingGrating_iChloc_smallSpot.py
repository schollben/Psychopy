from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
import serial, csv, time, math
import numpy as np
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
import UniversalLibrary as UL
print "initialized"

# ---------- Stimulus Description ---------- #
# A fullscreen drifting grating for 2pt orientation tuning
#---------- Monitor Properties ----------#

#Triggering type
triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True
#Optogenetic stimulation parameters
boardNum = 1
baseState = 0
stimTime = 0.1
UL.cbDConfigPort(boardNum, UL.FIRSTPORTA, UL.DIGITALOUT)
#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

mon= monitors.Monitor('dualmonitors') #gets the calib ration

# ---------- Stimulus Parameters ---------- #
numTrials = 1  #Run all the stims this many times
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=1 # number of blanks to show per trial.
changeDirectionAt = 1#When do we change movement directions? If 1, there should be no reversal. Setting to 0 causes instantaneous reversal, effectively inverting all stimIDs and angles.
stimDuration = 2
isi = 1
isRandom = 1 
initialDelay= 1

numOrientations = 1
orientations = numpy.arange(0,360,360.0/numOrientations)  #Remember, ranges in Python do NOT include the final value!
orientations = [0,180]
numOrientations = len(orientations)
stimOrder1 = np.empty([numTrials,numOrientations+1])
stimOrder2 = np.empty([numTrials,numOrientations+1])
stimOrder = np.empty([numTrials,2*(numOrientations+1)])
for i in range(0,numTrials):
    stimOrder1[i,:] = np.arange(numOrientations+1) # add 1 for blank
    stimOrder2[i,:] = np.arange(numOrientations+1)+numOrientations+1
    if isRandom:
        random.shuffle(stimOrder1[i,:])
        random.shuffle(stimOrder2[i,:])
stimOrder[:,0::2] = stimOrder1
stimOrder[:,1::2] = stimOrder2
stimOrder = stimOrder.astype(int)
print stimOrder
stiminfo = stimOrder.flatten()


# Grating parameter
temporalFreq = 4
spatialFreq = 0.16
#spatialFreq = 0.25
contrast = 1
textureType = 'sin'   #'sqr' = square wave, 'sin' = sinusoidal, 'sqrDutyCycle'
if textureType == 'sqrDutyCycle':
    dutyCycle = 5 # can be 1, 2, 3, 4, 6, 8,
    textureType = 1*numpy.ones((dutyCycle,1)); 
    textureType[1,:] = -1; 
startingPhase=0.0 # initial phase for gratingStim

#aperture and position parameters 
centerPoint = [-63,0]
stimSize = [300,300] #Size of grating in degrees
mon1= monitors.Monitor('projector') #gets the calibration for stimMonitor

projectorWinSize = [1000,1000]
spotSize = 125
#centerPoint = [-75.5,14]#screen about 113. deg wide and XX deg tall
#stimSize = [50,50] #Size of grating in degrees
# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)
myProjectorWin = visual.Window(size=(projectorWinSize),pos=(0,0),monitor=mon1,fullscr=True,screen=0, allowGUI=True, waitBlanking=True,color =[-1,-1,-1])

#set up box stimuli
boxStim = visual.Rect(win=myProjectorWin, units='pix', size=spotSize, pos=(25,0), lineColor = [-1,-1,-1], fillColor =[1,1,1],lineWidth = 1)
boxStim.setAutoDraw(True)

print "made window, setting up triggers"

#Set up the trigger behavior
trigger = None
if triggerType == "NoTrigger":
    import noTrigger
    trigger = noTrigger.noTrigger(None) 
elif triggerType == "SerialDaqOut" or triggerType == 'OutOnly':
    import serialTriggerDaqOut
    print 'Imported trigger serialTriggerDaqOut'
    trigger = serialTriggerDaqOut.serialTriggerDaqOut(serialPortName) 
    # determine the Next experiment file name
    expName=trigger.getNextExpName([dataPath,date])
    print "Trial name: ",expName
    if triggerType == 'OutOnly':
        trigger.readSer=False
    if adjustDurationToMatch2P:
        print "Waiting for serial Triggers"
        stimDuration = trigger.extendStimDurationToFrameEnd(stimDuration)
    # store the stimulus data and prepare the directory
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath,numTrials])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
print stimDuration


#create grating stim

gratingStim = visual.GratingStim(win=myWin,mask='circle', tex=textureType,units='deg',
    pos=[0,0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim.setAutoDraw(True)

grayStim = visual.GratingStim(win=myWin,units='deg',
    pos=[63, 0],size=[134,134], contrast=0, autoLog=False)
grayStim.setAutoDraw(True)

barTexture = numpy.ones([256,256,3]);
flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='None',units='pix',pos=[1940,540],size=(100,100))
flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x
clrctr=1;
print "made grating"

#run
optoClock = core.Clock()
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
print "\n",str(len(orientations)+doBlank), "stims will be run for",str(numTrials),"trials."
if nBlank > 1:
    print "Will run blank "+str(nBlank)+" times"
 # force a wait period of at least 5 seconds before first stim
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    gratingStim.setContrast(0)
    flipStim.setContrast(0)
    while clock.getTime()<initialDelay:
        myWin.flip()
for trial in range(0,numTrials): 
    #determine stim order
    print "Beginning Trial",trial+1
    for stimNumber in stimOrder[trial,:]:
        if stimNumber>numOrientations:           
            print "Blue light trial"
            optoClock.reset()
            print "Starting optogenetic stimulation"
            boxStim.fillColor = [1,1,1]
            while optoClock.getTime()<stimTime:
                print optoClock.getTime()
                UL.cbDOut(boardNum,UL.FIRSTPORTA,255)
                myProjectorWin.flip()
            print "Stopping optogenetic stimulation"
            UL.cbDOut(boardNum,UL.FIRSTPORTA,baseState)
        boxStim.fillColor = [-1,-1,-1]
        myProjectorWin.flip()
        time.sleep(.03)
        trigger.preStim(stimNumber+1)
        #display stim
        flipStim.setContrast(1)
        flipStim.setAutoDraw(True)
        if stimNumber>numOrientations:
            stimNumber = stimNumber-(numOrientations+1)
        # convert orientations to standard lab notation
        if stimNumber == len(orientations):
            gratingStim.setContrast(0)
            print "\tStim",stimNumber+1," (blank)"
        else:
            gratingStim.setContrast(contrast)
            gratingStim.ori = orientations[stimNumber]-90
            print "\tStim",stimNumber+1,orientations[stimNumber],'deg'
        clock.reset()
        while clock.getTime()<stimDuration:
            clrctr=clrctr+1;
            if clrctr%2==1:
                #flipStim.setColor((0,0,0),colorSpace='rgb')
                flipStim.setContrast(-1)
            else:
                #flipStim.setColor((1,1,1),colorSpace='rgb')
                flipStim.setContrast(1)
            gratingStim.setPhase(startingPhase+clock.getTime()*temporalFreq)
            #print startingPhase+clock.getTime()*temporalFreq
            trigger.preFlip(None)
            myWin.flip()
            myProjectorWin.flip()
            trigger.postFlip(None)
            
        #now do ISI
        if isi !=0:
            clock.reset()
            gratingStim.setContrast(0)
            flipStim.setContrast(0)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
            flipStim.setAutoDraw(False)
            while clock.getTime()<isi:
                #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
                myWin.flip()
        trigger.postStim(None)

trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'