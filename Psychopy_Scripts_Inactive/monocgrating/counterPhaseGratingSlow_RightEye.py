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

# ---------- Stimulus Parameters ---------- #
ori1=numpy.ones((8,),dtype=numpy.int)*0 + 22.5
ori2=numpy.ones((8,),dtype=numpy.int)*45 + 22.5
ori3=numpy.ones((8,),dtype=numpy.int)*90 + 22.5
ori4=numpy.ones((8,),dtype=numpy.int)*135 + 22.5
orientations = numpy.concatenate((ori1,ori2,ori3,ori4))
print orientations
phase = numpy.arange(0,1,0.125)
startingPhases = numpy.concatenate((phase,phase,phase,phase))
print startingPhases
stiminfo = numpy.array((orientations,startingPhases))

numTrials = 8 #Run all the stims this many times
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
stimDuration = 2
isi = 1
isRandom = 1
# Grating parameter
temporalFreq = .5 # freq of phase reversal

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
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
        
print stimDuration


#create grating stim
gratingStim = visual.GratingStim(win=myWin,tex='sin',units='deg',
    pos=[-68,0],size=[150,150], sf=0.08, contrast=1, autoLog=False)
gratingStim.setAutoDraw(True)

grayStim = visual.GratingStim(win=myWin,units='deg',
    pos=[68, 0],size=[134,134], contrast=0, autoLog=False)
grayStim.setAutoDraw(True)

barTexture = numpy.ones([256,256,3]);
flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='None',units='pix',pos=[-1920,540],size=(100,100))
flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x
clrctr=1;
print "made grating"

#run
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
cpClock=core.Clock()
print "\n",str(len(orientations)+doBlank), "stims will be run for",str(numTrials),"trials."
for trial in range(0,numTrials): 
    #determine stim order
    print "Beginning Trial",trial+1
    stimOrder = range(0,len(orientations)+doBlank)
    if isRandom:
        random.shuffle(stimOrder)
    for stimNumber in stimOrder:
        #display each stim
        trigger.preStim(stimNumber+1)
        #display stim
        flipStim.setContrast(1)
        flipStim.setAutoDraw(True)
        # convert orientations to standard lab notation
        if stimNumber == len(orientations):
            gratingStim.setContrast(0)
            print "\tStim",stimNumber+1," (blank)"
        else:
            gratingStim.setContrast(1)
            gratingStim.ori = orientations[stimNumber]-90
            startingPhase=startingPhases[stimNumber]
            print "\tStim",stimNumber+1,orientations[stimNumber],'deg  ',startingPhases[stimNumber]
        clock.reset()
        cpClock.reset()
        cpCtr=0;
        gratingStim.setPhase(startingPhase)
        while clock.getTime()<stimDuration:
            clrctr=clrctr+1;
            if clrctr%2==1:
                flipStim.setContrast(-1)
            else:
                flipStim.setContrast(1)
            if cpClock.getTime()>1/(temporalFreq*2.0):
                cpCtr=cpCtr+1;
                gratingStim.setPhase(startingPhase+cpCtr%2*0.5)
                cpClock.reset()                
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
            
        #now do ISI
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