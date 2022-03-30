from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
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

numTrials = 5 #Run all the stims this many times

#Params
stimDuration =1.5
temporalFreq = 4
textureType = 'sqr'
orientations=[0,90]
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
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,orientations,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
        
print stimDuration


#create grating stim
#gratingStim = visual.GratingStim(win=myWin,tex=textureType,units='deg',
#    pos=centerPoint,size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim=visual.GratingStim(myWin,mask='None', units='pix', tex='sqr', 
    size=[400,400], sf=0.008,contrast=1, pos=[0,0],
    autoLog=False)
gratingStim.setAutoDraw(True)
print "made grating"

#run
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
cpClock=core.Clock()
print "stims will be run for",str(numTrials),"trials."

initialDelay=4
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    gratingStim.setContrast(0)
    while clock.getTime()<initialDelay:
        myWin.flip()

for trial in range(0,numTrials): 
    #determine stim order
    print "Beginning Trial",trial+1
    
    numBlocks = 6*3 #retinotopic grid 6x3 = 320x320 pixels on each screen
    allBlocks = range(1,numBlocks+1)
    random.shuffle(allBlocks)
    print allBlocks
    for block in allBlocks:
        #display each stim
        trigger.preStim(block)
        #display stim
        for numOri in range(0,len(orientations)):
            gratingStim.ori = orientations[numOri]
            gratingStim.setContrast(1)
            print "\tBlock",block," Orientation",orientations[numOri]
            if block<7:
                position = [1920-(320/2)-320*(block-1) , 540-(320/2)]
            elif block>6 and block<13:
                position = [1920-(320/2)-320*(block-7) ,0]
            else:
                position = [1920-(320/2)-320*(block-13) , -540+(320/2)]
            gratingStim.pos = position
            clock.reset()
            cpClock.reset()
            cpCtr=0;
            while clock.getTime()<stimDuration:
                gratingStim.setPhase(clock.getTime()*4)
#                if cpClock.getTime()>1/(temporalFreq*2.0):
#                    cpCtr=cpCtr+1;
#                    gratingStim.setPhase(0+cpCtr%2*0.5)
#                    cpClock.reset()
                trigger.preFlip(None)
                myWin.flip()
                trigger.postFlip(None)
        

trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'