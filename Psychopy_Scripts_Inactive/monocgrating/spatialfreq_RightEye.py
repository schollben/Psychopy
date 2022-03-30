from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes

print "initialized"

# ---------- Stimulus Description ---------- #
# A fullscreen drifting grating for 2pt orientation tuning
#---------- Monitor Properties ----------#

#Triggering type
triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly'
serialPortName = 'COM2' 
adjustDurationToMatch2P=True

#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

mon= monitors.Monitor('dualmonitors') #gets the calibration

# ---------- Stimulus Parameters ---------- #
# ----------------------------------------#
numSFs = 8 
spatialFreq = [0.01,0.05,0.01,0.15,0.20,0.25,0.35,0.50]
orientations = [0,45,90,135]
stiminfo = orientations
#-----------------------------------------#

numTrials=6 #Run all the stims this many times

doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=1 # number of blanks to show per trial.
changeDirectionAt = .5#When do we change movement directions? If 1, there should be no reversal. Setting to 0 causes instantaneous reversal, effectively inverting all stimIDs and angles.
stimDuration =3 #use 4 because going to use 4 orientations
isi =3
isRandom =1
initialDelay=1

# Grating parameter
temporalFreq = 4
#spatialFreq = 0.1
contrast = 1
textureType = 'sin'   #'sqr' = square wave, 'sin' = sinusoidal, 'sqrDutyCycle'
if textureType == 'sqrDutyCycle':
    dutyCycle = 5 # can be 1, 2, 3, 4, 6, 8,
    textureType = 1*numpy.ones((dutyCycle,1)); 
    textureType[1,:] = -1; 
startingPhase=0.0 # initial phase for gratingStim

#aperture and position parameters 
stimSize = [150,150] #Size of grating in degrees

# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)


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
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
print stimDuration
changeDirectionTimeAt = stimDuration * changeDirectionAt


#create grating stim
gratingStim = visual.GratingStim(win=myWin,mask='None', tex=textureType,units='deg',
    pos=[67, 0],size=stimSize, autoLog=False)
gratingStim.setAutoDraw(True)

grayStim = visual.GratingStim(win=myWin,units='deg',
    pos=[-67, 0],size=[134,134], contrast=0, autoLog=False)
grayStim.setAutoDraw(True)

barTexture = numpy.ones([256,256,3]);
flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='None',units='pix',pos=[-1920,540],size=(100,100))
flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x
clrctr=1;
print "made grating"


#run
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
print "\n",str(len(spatialFreq)+doBlank), "stims will be run for",str(numTrials),"trials."
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
    stimOrder = range(0,len(spatialFreq)+doBlank)
    if nBlank > 1:
        blankID=len(spatialFreq)
        for ibl in range(1,nBlank):
            stimOrder.append(blankID)
    if isRandom:
        random.shuffle(stimOrder)
    for stimNumber in stimOrder:
        trigger.preStim(stimNumber+1)
        #display stim
        flipStim.setContrast(1)
        flipStim.setAutoDraw(True)
        # convert orientations to standard lab notation
        if stimNumber == len(spatialFreq):
            gratingStim.setContrast(0)
            print "\tStim",stimNumber+1," (blank)"
        else:
            gratingStim.setContrast(contrast)
            gratingStim.sf = spatialFreq[stimNumber]
            print "\tStim",stimNumber+1,spatialFreq[stimNumber],'cyc/deg'
        
        clock.reset()
        orientationOrder = range(0,len(orientations))
        for oriNumber in orientationOrder:
            gratingStim.ori = orientations[oriNumber]-90
            print orientations[oriNumber],'deg'
            clock.reset()
            while clock.getTime()<stimDuration:
                if clock.getTime()>changeDirectionTimeAt:
                    gratingStim.setPhase(startingPhase+changeDirectionTimeAt*temporalFreq - (clock.getTime()-changeDirectionTimeAt)*temporalFreq)
                else:
                    gratingStim.setPhase(startingPhase+clock.getTime()*temporalFreq)
                trigger.preFlip(None)
                myWin.flip()
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