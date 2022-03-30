from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
sys.path.append("../triggers") #path to trigger classes
from os import path
print "initialized"

#---------- Monitor Properties ----------#
mon= monitors.Monitor('dualmonitors') #gets the calibration for stimMonitor
mon.setDistance(25)
overwriteGammaCalibration=False
newGamma=0.479

# ---------- Stimulus Parameters ---------- #
#trials and duration
numDirections = 8 #typically 4, 8, or 16# 
directions = numpy.arange(0,360,360.0/numDirections) #Remember, ranges in Python do NOT include the final value!
numTrials=6#Run all the stims this many times
doBlank = 0#0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=1; # number of blanks to show per trial.
stimDuration =2.0
isi =2.0
isRandom =0
initialDelay=0# time in seconds to wait before first stimuli. Set to 0 to begin ASAP. 

# RDK parameters
backgroundColor = 1.0; #-1.0 is black, 0.0 is gray, and 1.0 is white
stimColor = -1.0; #-1.0 is black, 0.0 is gray, and 1.0 is white
temporalFreq = 4.0;
numberOfDots = 1000;
stimCoherence = 1;
sizeOfDots = 10; 
#aperture and position parameters 
centerPoint = [0,0] 
stimSize = [300,300] #Size of RDK in degrees

#Triggering type
#Can be any of:#"NoTrigger" - no triggering; stim will run freely
#"SerialDaqOut" - Triggering by serial port. Stim codes are written to the MCC DAQ.
# "OutOnly" - no input trigger, but does all output (to CED) and logging
#"DaqIntrinsicTrigger" - waits for stimcodes on the MCC DAQ and displays the appropriate stim ID
#triggerType = 'DaqIntrinsicTrigger'
triggerType = 'NoTrigger'
serialPortName = 'COM3' # ignored if triggerType is "None"
adjustDurationToMatch2P=True

#Experiment logging parameters
dataPath='x:/'
animalName='F1654_2014-05-09';
logFilePath =dataPath+animalName+'\\'+animalName+'.txt' #including filepath

# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#make a window
myWin = visual.Window(size=[1920,1080],rgb=(backgroundColor,backgroundColor,backgroundColor),monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=True,)
if overwriteGammaCalibration:
    myWin.setGamma(newGamma)
    print "Overwriting Gamma Calibration. New Gamma value:",newGamma

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
    expName=trigger.getNextExpName([dataPath,animalName])
    print "Trial name: ",expName
    if triggerType == 'OutOnly':
        trigger.readSer=False
    #Record a bunch of serial triggers and fit the stim duration to an exact multiple of the trigger time
    if adjustDurationToMatch2P:
        print "Waiting for serial Triggers"
        stimDuration = trigger.extendStimDurationToFrameEnd(stimDuration)
    # store the stimulus data and prepare the directory
    trigger.preTrialLogging([dataPath,animalName,expName,stimCodeName,directions,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
        
print stimDuration

# create RDK stim (must be done each stimulus presentation due to the direction of the stim not changing whenver the dir variable is changed
rdkStim = visual.DotStim(win=myWin, units='deg', nDots=numberOfDots, coherence=stimCoherence, fieldPos=centerPoint, fieldSize=stimSize, 
    fieldShape='sqr', dotSize=sizeOfDots, dotLife=-1, dir = 0.0, speed=temporalFreq, color=(stimColor, stimColor, stimColor), 
    colorSpace='rgb', opacity=1.0, contrast=1.0, signalDots='same', noiseDots='direction',autoLog=False);
rdkStim.setAutoDraw(True)

#run
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
print "\n",str(len(directions)+doBlank), "stims will be run for",str(numTrials),"trials."
if nBlank > 1:
    print "Will run blank "+str(nBlank)+" times"
 # force a wait period of at least 5 seconds before first stim
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    while clock.getTime()<initialDelay:
        myWin.flip()
for trial in range(0,numTrials): 
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,len(directions)+doBlank)
    if nBlank > 1:
        blankID=len(directions)
        for ibl in range(1,nBlank):
            stimOrder.append(blankID)
    if isRandom:
        random.shuffle(stimOrder)
    for stimNumber in stimOrder:
        # Set new stim direction
        rdkStim.setDir(directions[stimNumber]-90)
        
        #display each stim
        trigger.preStim(stimNumber+1)
        if stimNumber == len(directions):
            print "\tStim",stimNumber+1," (blank)"
        else:
            print "\tStim",stimNumber+1,directions[stimNumber],'deg'
        clock.reset()
        while clock.getTime()<stimDuration:
            if stimNumber != len(directions):
                rdkStim.setContrast(1)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
            
        #now do ISI
        if isi !=0:
            clock.reset()
            trigger.preFlip(None)
            rdkStim.setContrast(0)
            myWin.flip()
            trigger.postFlip(None)
            while clock.getTime()<isi:
                #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
                myWin.flip()
        trigger.postStim(None)

trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'