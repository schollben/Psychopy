from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
import numpy as np
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
print "initialized"


#Triggering type
triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True

#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

mon= monitors.Monitor('dualmonitors') #gets the calibration

numTrials = 6 #Run all the stims this many times 

#Params
doBlank=1
stimDuration = 2 #  for each orientations
temporalFreq = 4
isi=2
textureType = 'sqr'
oriChangetimes = numpy.arange(0,stimDuration,0.01111)
print oriChangetimes

# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=True)
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
    #Record a bunch of serial triggers and fit the stim duration to an exact multiple of the trigger time
    if adjustDurationToMatch2P:
        print "Waiting for serial Triggers"
        stimDuration = trigger.extendStimDurationToFrameEnd(stimDuration)
    # store the stimulus data and prepare the directory
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stimDuration,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
        
print stimDuration

chx=np.array([[1,-1],[-1,1]]);


#create grating stim
#gratingStim = visual.GratingStim(win=myWin,tex=textureType,units='deg',
#    pos=centerPoint,size=stimSize, sf=spatialFreq, autoLog=False)
# make mask gauss??
gratingStim1=visual.GratingStim(myWin,mask='None', units='pix', tex=chx, 
    size=[240,240], sf=0.008,opacity = 1,
    autoLog=False)
gratingStim1.setAutoDraw(True) 
gratingStim2=visual.GratingStim(myWin,mask='None', units='pix', tex='sqr', 
    size=[240,240], sf=0.008,opacity = 0.5,
    autoLog=False)
gratingStim2.setAutoDraw(False) 
clrctr=1;
print "made grating"

#run
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
cpClock=core.Clock()
print "stims will be run for",str(numTrials),"trials."

initialDelay=0
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    gratingStim1.setContrast(0)
    gratingStim2.setContrast(0)
    while clock.getTime()<initialDelay:
        myWin.flip()

for trial in range(0,numTrials): 
    #determine stim order
    print "Beginning Trial",trial+1
    
    numBlocks = 8*4   #retinotopic grid 6x3 = 320x320 pixels on each screen
    # now doing 8 x 4 grid 240 x 240 pixels on each screen
    
    allBlocks = range(1,numBlocks+1+doBlank)
    random.shuffle(allBlocks)
    print allBlocks
    for block in allBlocks:
        #display each stim
        trigger.preStim(block)
        #display stim
        if block==numBlocks+1 and doBlank==1:
            gratingStim1.setContrast(0)
        else:
            gratingStim1.setContrast(1)
        print "\tBlock",block
        if block<9:
            position = [-1920+(240/2)+240*(block-1) , 270/2 + 270]
        elif block>8 and block<17:
            position = [-1920+(240/2)+240*(block-1-8) , 270/2]
        elif block>16 and block<25:
            position = [-1920+(240/2)+240*(block-1-16) ,-270/2]
        else:
            position = [-1920+(240/2)+240*(block-1-24) , -270/2 - 240]
        
        gratingStim1.pos = position
        
        clock.reset()
        cpClock.reset()
        cpCtr=0;
        gratingStim1.setPhase(0)
        while clock.getTime()<stimDuration:
            gratingStim1.ori = clock.getTime()*(360/stimDuration)
            gratingStim1.setPhase(clock.getTime()*temporalFreq)
            clrctr=clrctr+1;
            #if cpClock.getTime()>1/(temporalFreq*2.0):
            #    cpCtr=cpCtr+1;
            #    gratingStim1.setPhase(clock.getTime()*temporalFreq+cpCtr%2*0.5)
            #    cpClock.reset()
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
                
        #now do ISI
        clock.reset()
        gratingStim1.setContrast(0)
#        flipStim.setContrast(0)
        trigger.preFlip(None)
        myWin.flip()
        trigger.postFlip(None)
        while clock.getTime()<isi:
            #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
            myWin.flip()
        trigger.postStim(None)

trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'