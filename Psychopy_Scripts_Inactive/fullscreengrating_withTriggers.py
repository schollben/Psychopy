from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes


#---------- Monitor Properties ----------#
mon= monitors.Monitor('dualmonitors') #gets the calibration for stimMonitor
mon.setDistance(25)
overwriteGammaCalibration=False
newGamma=0.479

#input parameters
numberOfTrials=10

temporalFreq=4
spatialFreq=0.1
spinPeriodInSeconds = 60
spinDirection = -1; #1 is clockwise, -1 is counter-clockwise
if(spinDirection == -1): # +1 is clockwise (from 0 to 179deg), +2 is clockwise (from 180 to 359deg)
    stimIDs = [1,2]
else:                         # +3 is counter-clockwise (from 180 to 1 deg), +4 is counter-clockwise (from 0 to 181 deg)
    stimIDs = [3,4]
textureType = 'sin' #'sqr' = square wave, 'sin' = sinusoidal
initialDelay = 0 # time in seconds to wait before first stimuli. Set to 0 to begin ASAP. 


#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
animalName = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+animalName+'\\'+animalName+'.txt' #including filepath

# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#Triggering type
#Can be any of:#"NoTrigger" - no triggering; stim will run freely
#"SerialDaqOut" - Triggering by serial port. Stim codes are written to the MCC DAQ.
# "OutOnly" - no input trigger, but does all output (to CED) and logging
#"DaqIntrinsicTrigger" - waits for stimcodes on the MCC DAQ and displays the appropriate stim ID

#triggerType = 'DaqIntrinsicTrigger'
triggerType = 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "None"
adjustDurationToMatch2P=False

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
    expName=trigger.getNextExpName([dataPath,animalName])
    print "Trial name: ",expName
    if triggerType == 'OutOnly':
        trigger.readSer=False
    #Record a bunch of serial triggers and fit the stim  to an exact multiple of the trigger time
    if adjustDurationToMatch2P:
        print "Waiting for serial Triggers"
        spinPeriodInSeconds = trigger.extendStimDurationToFrameEnd(spinPeriodInSeconds)
    # store the stimulus data and prepare the directory
    trigger.preTrialLogging([dataPath,animalName,expName,stimCodeName,stimIDs,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType


#calculated parameters
spinDegreesPerSecond = 360 / spinPeriodInSeconds

#make a window
mywin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)
if overwriteGammaCalibration:
    mywin.setGamma(newGamma)
    print "Overwriting Gamma Calibration. New Gamma value:",newGamma

#create grating
stim1 = visual.PatchStim(win=mywin,tex=textureType,mask='none',units='deg',pos=(0,0),size=(300,300), sf=spatialFreq)
stim1.setAutoDraw(True)

# wait for an initial delay
clock = core.Clock()
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    stim1.setContrast(0)
    while clock.getTime()<initialDelay:
        mywin.flip()

#run
duration=numberOfTrials*spinPeriodInSeconds #in seconds
print("Stim Duration is "+str(duration)+" seconds")
currentTrial=0
stim1.setContrast(1)
clock.reset()
while clock.getTime()<duration:        
    
    # output trigger at the beginning of every trial
        if clock.getTime()>=currentTrial*(spinPeriodInSeconds/2.0):
            currentTrial=currentTrial+1;
            print("Direction Trial "+str(math.ceil(currentTrial/2.0)))+" / Orientation Trial "+str(currentTrial)
            currentStimID = 2+spinDirection+(currentTrial-1)%2
            trigger.preStim(currentStimID)
            trigger.preFlip(None)
            mywin.flip()
            trigger.postFlip(None)
            trigger.postStim(None)
        
        newPhase = clock.getTime()*temporalFreq
        newOri = spinDirection*clock.getTime()*spinDegreesPerSecond-90
        stim1.setPhase(newPhase)
        stim1.setOri(newOri)
        mywin.flip()

print clock.getTime()
        