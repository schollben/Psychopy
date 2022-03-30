from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
import serial, csv, time, math
import numpy as np
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
import UniversalLibrary as UL
print "initialized"
#---------- Monitor Properties ----------#
mon= monitors.Monitor('dualmonitors') #gets the calib ration
mon.setDistance(26)
overwriteGammaCalibration=False
newGamma=0.479

#time parameters
numTrials = 5; # how many trials
movementPeriod = 2 #how long it takes for a bar to move from startPoint to endPoint
initialDelay = 0; # time in seconds to wait before first stimuli. Set to 0 to begin ASAP. 
isi = 0.5
stimOrder = np.empty([numTrials,5])
for i in range(0,numTrials):
    stimOrder[i,:] = np.arange(5)
    #random.shuffle(stimOrder[i,:])
stimOrder=stimOrder.astype(int)
#bar parameters
orientation =112.5  #0 is horizontal, 90 is vertical. 45 goes from up-left to down-right.
barColor = 0; #1 for white, 0 for black, 0.5 for low contrast white, etc.
spatialFreq = 0.06
#position parameters
centerPoint = [-65,11] #center of screen is [0,0] (degrees).
travel = 4/spatialFreq
startPoint = -travel #bar starts this far from centerPoint (in degrees)
print startPoint
endPoint = travel; #bar moves to this far from centerPoint (in degrees)
print endPoint
stimSize = (150,1/spatialFreq/2) # (180,4) #First number is longer dimension no matter what the orientation is. - typically is (180,4)

#flashing parameters
flashPeriod = 1.0 #0.2 #amount of time it takes for a full cycle (on + off). Set to 1 to get static drifting bar (no flash). 
dutyCycle = 1.0 #0.5 #Amount of time flash bar is "on" vs "off". 0.5 will be 50% of the time. Set to 1 to get static drifting bar (no flash). 

#Experiment logging parameters
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)
triggerType = 'OutOnly';
serialPortName = 'COM2' # ignored if triggerType is "None"
adjustDurationToMatch2P=True
stiminfo = stimOrder.flatten()
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
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath,numTrials])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType


#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)

#create bar stim
#barTexture = numpy.ones([256,256,3])*barColor;
barTexture = numpy.ones([256,256,3]);
barStim = visual.PatchStim(win=myWin,tex=barTexture,mask='none',units='deg',pos=centerPoint,size=stimSize,ori=orientation)
barStim.setContrast(0)
barStim.setAutoDraw(True)
barStim.setColor(barColor*255, 'rgb255')

# wait for an initial delay
clock = core.Clock()
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    while clock.getTime()<initialDelay:
        myWin.flip()
duration = movementPeriod
#run
print("Stim Duration is "+str(movementPeriod)+" seconds")
for trial in range(0,numTrials): 
    #determine stim order
    print "Beginning Trial",trial+1
    for stimNumber in stimOrder[trial,:]:
        clock.reset()
        trigger.preStim(stimNumber+1)
        print "Stim number",stimNumber+1
        if stimNumber==4:
            barStim.setContrast(0)
        elif 1<stimNumber<4:
            barStim.setContrast(-1)
        elif stimNumber<2:
            barStim.setContrast(1)
        while clock.getTime()<duration:
            if stimNumber==0 or stimNumber==2:
                posLinear = (clock.getTime() % movementPeriod) / movementPeriod * (startPoint-endPoint) + endPoint; #what pos we are at in degrees
            else:
                posLinear = (clock.getTime() % movementPeriod) / movementPeriod * (endPoint-startPoint) + startPoint; #what pos we are at in degrees
            posX = posLinear*math.sin(orientation*math.pi/180)+centerPoint[0]
            posY = posLinear*math.cos(orientation*math.pi/180)+centerPoint[1]
            barStim.setPos([posX,posY])
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
        if isi !=0:
                clock.reset()
                barStim.setContrast(0)
                trigger.preFlip(None)
                myWin.flip()
                trigger.postFlip(None)
                while clock.getTime()<isi:
                    #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
                    myWin.flip()
trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'