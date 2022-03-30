from psychopy import visual, logging, core, monitors
import pylab, math, serial, sys, numpy, random
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
from os import path

#---------- Monitor Properties ----------#
mon= monitors.Monitor('dualmonitors') #gets the calibration for stimMonitor
mon.setDistance(26)
overwriteGammaCalibration=False
newGamma=0.479

#bar parameters
numOrientations = 8# 8 #typically 4, 8, or 16# 
animalOrientation=0;
orientations = numpy.arange(0,360,360.0/numOrientations) #Remember, ranges in Python do NOT include the final value!
stimOrder = range(0,len(orientations))
barColor = 1; #1 for white, 0 for black, 0.5 for gray, 0 for black, etc.
backGroundColor =0; #1 for white, 0 for black, 0.5 for gray, 0 for black, etc.
backGroundBarColor=0.5; # used as background if a bar is presented instead of edge
isRandom=True;

#position parameters
edgeWidth = 360 # use 360 for edge and 4-8 for moving Bar
centerPoint = [-60,0] #center of screen is [0,0] (degrees).
#startPoint = -125-edgeWidth/2; #bar starts this far from centerPoint (in degrees)
#endPoint = 0+edgeWidth/2; #bar moves to this far from centerPoint (in degrees)
startPoint=-60-edgeWidth/2
endPoint=60-edgeWidth/2
stimSize = (3600,0+edgeWidth) # (180,4) #First number is longer dimension no matter what the orientation is. - typically is (180,4)
# for elevation (stim 5)(-45 45) works well, for azimuth (stim 3), -125,125 works for both monitors, if running contra monitor only, use [0 125], for stim 7 run [-125 0]


#time parameters
numberOfTrials = 6; # how many trials
initialDelay =0; #5 time in seconds to wait before first stimuli. Set to 0 to begin ASAP. 
movementPeriod = 8 #how long it takes for a bar to move from startPoint to endPoint. Specify -1 if to overide and automatically set based on degrees traveled per second
if(movementPeriod == -1):
    DegreesPerSecond = 22.5; #22.5 is the normal speed we've been using (180.0 Degrees /8.0s cycle)
    movementPeriod = (endPoint-startPoint)/DegreesPerSecond
    print("Movement Period: "+str(movementPeriod)+"s");

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
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,orientations,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType


#make a window
barColorArray = (2*barColor-1)*numpy.ones(3);
backGroundColorArray = (2*backGroundColor-1)*numpy.ones(3);
#mywin = visual.Window(monitor=mon,fullscr=True,screen=1,rgb=backGroundColorArray)
mywin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)

if overwriteGammaCalibration:
    myWin.setGamma(newGamma)
    print "Overwriting Gamma Calibration. New Gamma value:",newGamma

#create bar stim
#barTexture = numpy.ones([256,256,3])*barColor;
barTexture = numpy.ones([256,256,3]);
barStim = visual.GratingStim(win=mywin,tex=barTexture,mask='none',units='deg',pos=centerPoint,size=stimSize)
barStim.setContrast(1)
barStim.setAutoDraw(True)
barStim.setColor(backGroundColor*255, 'rgb255')
if(edgeWidth!=360):
    mywin.setColor(backGroundBarColor*255, 'rgb255')
    barStim.setColor(backGroundBarColor*255, 'rgb255')

# wait for an initial delay
clock = core.Clock()
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    while clock.getTime()<initialDelay:
        mywin.flip()

#run
duration=2*numberOfTrials*numOrientations*movementPeriod #in seconds
print("Stim Duration is "+str(duration)+" seconds")
currentStim=0
currentTrial=0
currentOrientationIndex=0
clock.reset()
while clock.getTime()<duration:
    # output trigger at the beginning of every trial
    if clock.getTime()>=currentStim*movementPeriod:
        currentStim=currentStim+1;
        stimID=(((currentStim+1)/2)-1)%numOrientations;
        if ((currentStim-1)%(2*numOrientations)==0): #checks if new trial
            currentTrial = currentTrial+1;
            if isRandom:
                random.shuffle(stimOrder)
        trigger.preStim(1+stimOrder[stimID])
        trigger.preFlip(None)
        trigger.postFlip(None)
        trigger.postStim(None)
        isEvenTrial=1-(currentStim%2)
        if isEvenTrial:
            if(edgeWidth==360):
                mywin.setColor(barColor*255, 'rgb255')
            mywin.flip()
            barStim.setColor(backGroundColor*255, 'rgb255')
        else:
            if(edgeWidth==360):
                mywin.setColor(backGroundColor*255, 'rgb255')
            mywin.flip()
            barStim.setColor(barColor*255, 'rgb255')
        print("Trial "+str(currentTrial)+" / Phase "+str(1+isEvenTrial)+" / Stim "+str(1+stimOrder[stimID])+" - "+str(orientations[stimOrder[stimID]])+" Deg") 
#        core.wait(0.01)

    currentPeriodTime = clock.getTime()
    barStim.ori = animalOrientation+orientations[stimOrder[stimID]]
    if (currentPeriodTime<currentStim*movementPeriod):
        posLinear = (currentPeriodTime % movementPeriod) / movementPeriod * (endPoint-startPoint) + startPoint; #what pos we are at in degrees
        posX = posLinear*math.sin(barStim.ori*math.pi/180)+centerPoint[0]
        posY = posLinear*math.cos(barStim.ori*math.pi/180)+centerPoint[1]
        barStim.setPos([posX,posY])
        mywin.flip()
   
print clock.getTime()
    