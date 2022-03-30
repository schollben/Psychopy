from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes

print "initialized"

# ---------- Stimulus Description ---------- #
# A fullscreen drifting grating for 2pt orientation tuning
#---------- Monitor Properties ----------#

#Triggering type
triggerType = 'NoTrigger' # 'SerialDaqOut' OR 'OutOnly' OR 'NoTrigger'
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True

#Experiment logging parameters
#--------#
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath
#--------#


mon= monitors.Monitor('dualmonitors') #gets the calibration
#----------distance off by 2x, 50 cm == 25 cm

# ---------- Stimulus Parameters ---------- #
# each has length of total number stimuli (not including blank)
# here there is 8 phases and 2 orientations (0,180)
numphases = 2
spatialphases = [0,0]
spatialphases = numpy.concatenate((spatialphases,spatialphases))
ori1 = numpy.ones(numphases) * 0
ori2 = numpy.ones(numphases) * 180
orientations =  numpy.concatenate((ori1,ori2))
#--------#
stiminfo=numpy.array((orientations,spatialphases))
#--------# 

numTrials=100
doBlank = 0 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=0 # number of blanks to show per trial.
changeDirectionAt = 1  #1 no reversal
stimDuration =1
isi =1
isRandom =0

initialDelay=0

# Grating parameters
temporalFreq = 4
spatialFreq = 0.07
contrast = 1
textureType = 'sqr'   #'sqr' = square wave, 'sin' = sinusoidal,'sqrDutyCycle'

#aperture and position parameters 
#fullfield in degrees for dual setup: 67.7deg x 2
stimSize = [100,100] #Size of grating in degrees, basically full field
centerpos = 68 #visual degrees off by 2 (33.15 x 2)

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
    #--------#
    expName=trigger.getNextExpName([dataPath,date])
    #--------#
    print "Trial name: ",expName
    if triggerType == 'OutOnly':
        trigger.readSer=False
    #Record a bunch of serial triggers and fit the stim duration to an exact multiple of the trigger time
    if adjustDurationToMatch2P:
        print "Waiting for serial Triggers"
        stimDuration = trigger.extendStimDurationToFrameEnd(stimDuration)
    # store the stimulus data and prepare the directory
    #--------#
#    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath]) 
    #--------#
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
        
changeDirectionTimeAt = stimDuration * changeDirectionAt



#create grating stimulus 1- left eye
gratingStim1 = visual.GratingStim(win=myWin,tex=textureType,units='deg',
    pos=[-centerpos, 0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim1.setAutoDraw(True)

#create grating stimulus 2- right eye (phase changes here)
gratingStim2 = visual.GratingStim(win=myWin,tex=textureType,units='deg',
    pos=[centerpos, 0],size=stimSize, sf=spatialFreq, autoLog=False)
gratingStim2.setAutoDraw(True)

#create corner patch to see frames
barTexture = numpy.ones([256,256,3]);
flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='None',units='pix',pos=[-1920,540],size=(100,100))
flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x
clrctr=1;

print "made grating"
#run
clock = core.Clock() # make one clock, instead of a new instance every time. 

totalStims = len(spatialphases)+4 #4 monocular stims
print "\n",str(totalStims), "stims will be run for",str(numTrials),"trials."

if nBlank > 1:
    print "Will run blank "+str(nBlank)+" times"
 # force a wait period of at least 5 seconds before first stim
 
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    gratingStim1.setContrast(0)
    gratingStim2.setContrast(0)
    flipStim.setContrast(0)
    while clock.getTime()<initialDelay:
        myWin.flip()
for trial in range(0,numTrials): 
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,totalStims)
    print stimOrder
    blankID=totalStims-1
    if isRandom:
        random.shuffle(stimOrder)
        print stimOrder
    for stimNumber in stimOrder:
        #
        trigger.preStim(stimNumber+1)
        #display stim
        flipStim.setContrast(1)
        flipStim.setAutoDraw(True)
        # convert orientations to standard lab notation
        if stimNumber ==blankID:
            gratingStim1.setContrast(contrast)
            gratingStim2.setContrast(contrast)
            gratingStim1.ori = 0
            gratingStim2.ori = 0
            gratingStim1phase = 0
            gratingStim2phase = 0
            print "binoc stimulus!"
        elif stimNumber==blankID-4:
            gratingStim1.setContrast(contrast)
            gratingStim2.setContrast(0)
            gratingStim1.ori = 0
            gratingStim2.ori = 0
            gratingStim1phase = 0
            gratingStim2phase = 0
            print "\tStim",stimNumber+1,"Left Eye"
        elif stimNumber==blankID-3:
            gratingStim1.setContrast(contrast)
            gratingStim2.setContrast(0)
            gratingStim1.ori = 180
            gratingStim2.ori = 180
            gratingStim1phase = 0
            gratingStim2phase = 0
            print "\tStim",stimNumber+1,"Left Eye"
        elif stimNumber==blankID-2:
            gratingStim1.setContrast(0)
            gratingStim2.setContrast(contrast)
            gratingStim1.ori = 0
            gratingStim2.ori = 0
            gratingStim1phase = 0
            gratingStim2phase = 0
            print "\tStim",stimNumber+1,"Right Eye"
        elif stimNumber==blankID-1:
            gratingStim1.setContrast(0)
            gratingStim2.setContrast(contrast)
            gratingStim1.ori = 180
            gratingStim2.ori = 180
            gratingStim1phase = 0
            gratingStim2phase = 0
            print "\tStim",stimNumber+1,"Right Eye"
        else:
            gratingStim1.setContrast(contrast)
            gratingStim2.setContrast(contrast)
            gratingStim1.ori = orientations[stimNumber]
            gratingStim2.ori = orientations[stimNumber]
            gratingStim1phase = 0
            gratingStim2phase = 0
            print "binoc stimulus!"
        clock.reset()
        while clock.getTime()<stimDuration:
            clrctr=clrctr+1;
            if clrctr%2==1:
                flipStim.setContrast(-1)
            else:
                flipStim.setContrast(1)
            #drift stimulus here
            gratingStim1.setPhase(gratingStim1phase+clock.getTime()*temporalFreq)
            gratingStim2.setPhase(gratingStim2phase+clock.getTime()*temporalFreq)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
            
        #now do ISI
        if isi !=0:
            clock.reset()
            gratingStim1.setContrast(0)
            gratingStim2.setContrast(0)
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