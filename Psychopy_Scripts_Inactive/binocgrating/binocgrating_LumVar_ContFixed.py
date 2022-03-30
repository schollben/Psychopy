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
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True

#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

mon= monitors.Monitor('dualmonitors') #gets the calibration

# ---------- Stimulus Parameters ---------- #
numTrials= 1 #Run all the stims this many times
stimDuration =.9

drift = 0 #add drift?
initialDelay=1
isi = 0

# ---------- Stimulus code begins here ---------- #
stiminfo = 0
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




#values for gratings
LumVal = [-0.90, -0.75, -0.60, -0.45, -0.30, -0.15, 0]
cont =       0.80
SF =        [0.02, 0.04, 0.08, 0.16, 0.032]
phases =  numpy.arange(0,1,0.125)

#binocular combinations for contrasts
binocVals=numpy.array([]);
for j in LumVal:
    for k in LumVal:
        binocVals = numpy.concatenate((binocVals,numpy.array([j,k])));
binocVals = binocVals.reshape(len(LumVal)*len(LumVal),2) 
 

#SF/binocular phase combinations
gratVals=numpy.array([]);
for j in SF:
    for k in phases:
        gratVals = numpy.concatenate((gratVals,numpy.array([j,k])));
gratVals = gratVals.reshape(len(phases)*len(SF),2)
totalStim = len(binocVals)*len(gratVals);
print totalStim

#repmat binocVals and gratVals by the length of gratVals (the number of unique grating values being used)
stimulusParams = numpy.tile(gratVals,(1,len(binocVals)));
stimulusParams = stimulusParams.reshape(totalStim,2)
print len(stimulusParams)

binocParams = numpy.tile(binocVals,(len(gratVals),1)); 
print len(binocParams)

#randomize order of combinations and then save into text file
stimIDs = range(0,totalStim)
random.shuffle(stimIDs)
print len(stimIDs)

numpy.savetxt(dataPath+date+'\\'+expName+'\\stimulusParams.txt',stimulusParams,fmt='%f')
numpy.savetxt(dataPath+date+'\\'+expName+'\\binocParams.txt',binocParams,fmt='%f')
numpy.savetxt(dataPath+date+'\\'+expName+'\\stimIDs.txt',stimIDs,fmt='%f')



changeDirectionAt = 0.5#When do we change movement directions? If 1, there should be no reversal. Setting to 0 causes instantaneous reversal, effectively inverting all stimIDs and angles.

clock = core.Clock() # make one clock, instead of a new instance every time. Use 
for trial in range(0,numTrials):
    
    print "Beginning Trial",trial+1
    
    for stimNumber in stimIDs:
        
        print stimNumber+1
        trigger.preStim(stimNumber+1)
        
        #grating parameters
        spatialFreq = stimulusParams[stimNumber,0]
        phase = stimulusParams[stimNumber,1]
        
        # right eye grating
        meanLuminanceR = binocParams[stimNumber,0]
        luminanceRangeR = cont
        
        a = meanLuminanceR - (1+meanLuminanceR)*luminanceRangeR;
        b = meanLuminanceR + (1+meanLuminanceR)*luminanceRangeR;
        textureType=numpy.array([a,b])[numpy.newaxis]
        gratingStim1 = visual.GratingStim(win=myWin,mask='circle', tex=textureType,units='deg',size=[120,120], sf=spatialFreq, autoLog=False)
        gratingStim1.pos = [67,0]
        gratingStim1.ori = 0
    
        # left eye grating
        meanLuminanceL = binocParams[stimNumber,1]
        luminanceRangeL = cont
        
        a = meanLuminanceL - (1+meanLuminanceL)*luminanceRangeL;
        b = meanLuminanceL + (1+meanLuminanceL)*luminanceRangeL;
        textureType=numpy.array([a,b])[numpy.newaxis]
        gratingStim2 = visual.GratingStim(win=myWin,mask='circle', tex=textureType,units='deg',size=[120,120], sf=spatialFreq, autoLog=False)
        gratingStim2.pos = [-67,0]
        gratingStim2.ori = 0
    
        #print parameters
        print luminanceRangeR, luminanceRangeL, spatialFreq, phase
    
        gratingStim1.setAutoDraw(True)
        gratingStim2.setAutoDraw(True)
        
        changeDirectionTimeAt = stimDuration * changeDirectionAt
        
        
        clock.reset()
        while clock.getTime()<stimDuration:
            if clock.getTime()>changeDirectionTimeAt:
                gratingStim1.setPhase(phase)# + changeDirectionTimeAt*2 - (clock.getTime()-changeDirectionTimeAt)*2)
                gratingStim2.setPhase(0)# + changeDirectionTimeAt*2 - (clock.getTime()-changeDirectionTimeAt)*2)
            else:
                gratingStim1.setPhase(phase)# + clock.getTime()*2)
                gratingStim2.setPhase(0)# + clock.getTime()*2)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
        
        
        
        
        #now do ISI
        if isi !=0:
            clock.reset()
            gratingStim1.setContrast(0)
            gratingStim2.setContrast(0)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
            while clock.getTime()<isi:
                #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
                myWin.flip()
        trigger.postStim(None)

trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'





