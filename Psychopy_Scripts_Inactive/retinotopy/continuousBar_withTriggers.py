from psychopy import visual, logging, core, monitors
import pylab, math, serial, sys, numpy
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
from os import path

#---------- Monitor Properties ----------#
mon= monitors.Monitor('dualmonitors') #gets the calibration
mon.setDistance(26)
overwriteGammaCalibration=False
newGamma=0.479

#time parameters
numberOfTrials = 10; # how many trials
movementPeriod = 1*16; #how long it takes for a bar to move from startPoint to endPoint
initialDelay = 0; #5 time in seconds to wait before first stimuli. Set to 0 to begin ASAP. 

#bar parameters
animalOrientation=0;
stimID = 1; # uses driftGrating standard (1 - Horizontal Bar (Drifting Down), 5 - Horizontal Bar (Drifting Up), 3 - Vertical Bar (Drifting Left), 7 - Vertical Bar (Drifting Right)
orientation =animalOrientation+(stimID-1)*45+180 #0 is horizontal, 90 is vertical. 45 goes from up-left to down-right.
barColor = 1; #1 for white, 0 for black, 0.5 for gray, 0 for black, etc.
backGroundColor = 0; #1 for white, 0 for black, 0.5 for gray, 0 for black, etc.

#position parameters
centerPoint = [0,0] #center of screen is [0,0] (degrees).
startPoint = -45; #bar starts this far from centerPoint (in degrees)
endPoint = 45; #bar moves to this far from centerPoint (in degrees)
stimSize = (300,4) # (180,4) #First number is longer dimension no matter what the orientation is. - typically is (180,4)
# for elevation (stim 5)(-45 45) works well, for azimuth (stim 3), -125,125 works for both monitors, if running contra monitor only, use [0 125], for stim 7 run [-125 0]


#flashing parameters
flashPeriod = 0.2 #0.2 #amount of time it takes for a full cycle (on + off). Set to 1 to get static drifting bar (no flash). 
dutyCycle = 0.5 #0.5 #Amount of time flash bar is "on" vs "off". 0.5 will be 50% of the time. Set to 1 to get static drifting bar (no flash). 

#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#Triggering type
#Can be any of:#"NoTrigger" - no triggering; stim will run freely
#"SerialDaqOut" - Triggering by serial port. Stim codes are written to the MCC DAQ.
# "OutOnly" - no input trigger, but does all output (to CED) and logging
#"DaqIntrinsicTrigger" - waits for stimcodes on the MCC DAQ and displays the appropriate stim ID
#triggerType = 'DaqIntrinsicTrigger'
triggerType = 'OutOnly';
serialPortName = 'COM2' # ignored if triggerType is "None"
adjustDurationToMatch2P=True

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
    #Record a bunch of serial triggers and fit the stim  to an exact multiple of the trigger time
    if adjustDurationToMatch2P:
        print "Waiting for serial Triggers"
        movementPeriod = trigger.extendStimDurationToFrameEnd(movementPeriod)
    # store the stimulus data and prepare the directory
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stimID,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType


#make a window
mywin = visual.Window(monitor=mon,fullscr=True,screen=1,rgb=(2*backGroundColor-1)*numpy.array([1.0,1.0,1.0]))
if overwriteGammaCalibration:
    myWin.setGamma(newGamma)
    print "Overwriting Gamma Calibration. New Gamma value:",newGamma

#create bar stim
#barTexture = numpy.ones([256,256,3])*barColor;
barTexture = numpy.ones([256,256,3]);
barStim = visual.PatchStim(win=mywin,tex=barTexture,mask='none',units='deg',pos=centerPoint,size=stimSize,ori=orientation)
barStim.setContrast(0)
barStim.setAutoDraw(True)
barStim.setColor(barColor*255, 'rgb255')

# wait for an initial delay
clock = core.Clock()
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    while clock.getTime()<initialDelay:
        mywin.flip()

#run
duration=numberOfTrials*movementPeriod #in seconds
print("Stim Duration is "+str(duration)+" seconds")
currentTrial=0
clock.reset()
while clock.getTime()<duration:
    # output trigger at the beginning of every trial
    if clock.getTime()>=currentTrial*movementPeriod:
        currentTrial=currentTrial+1;
        print("Trial "+str(currentTrial))
        trigger.preStim(stimID)
        trigger.preFlip(None)
        mywin.flip()
        trigger.postFlip(None)
        trigger.postStim(None)
    
    posLinear = (clock.getTime() % movementPeriod) / movementPeriod * (endPoint-startPoint) + startPoint; #what pos we are at in degrees
    if (clock.getTime()/flashPeriod) % (1.0) < dutyCycle:
        barStim.setContrast(1)
    else:
        barStim.setContrast(-1)
    posX = posLinear*math.sin(orientation*math.pi/180)+centerPoint[0]
    posY = posLinear*math.cos(orientation*math.pi/180)+centerPoint[1]
    barStim.setPos([posX,posY])
    mywin.flip()
   
print clock.getTime()
    