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
orientations = 90
stiminfo = orientations

numTrials= 2 #Run all the stims this many times

doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=1 # number of blanks to show per trial.
changeDirectionAt = 0.5#When do we change movement directions? If 1, there should be no reversal. Setting to 0 causes instantaneous reversal, effectively inverting all stimIDs and angles.
stimDuration =2
isi =2
isRandom =1
initialDelay=1

# Grating parameter
temporalFreq1 = 4
temporalFreq2 = 6
spatialFreq = 0.07

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




#creat stimulus IDs and lookup table
meanLuminanceValues = [0,-0.45,-0.9];
contrastValues = [.9,0.5,0.1];
stimulusMatrix=numpy.array([]);
for ii in meanLuminanceValues:
    for jj in contrastValues: 
        stimulusMatrix = numpy.concatenate((stimulusMatrix,numpy.array([ii,jj])));
stimulusMatrix = stimulusMatrix.reshape(9,2)
print stimulusMatrix
cnt = 0;
stimulusMatrixLength = range(9)
LeftParams = numpy.array([]);
RightParams = numpy.array([]);
for ii in stimulusMatrixLength:
    for jj in stimulusMatrixLength:
        LeftParams = numpy.concatenate((LeftParams,stimulusMatrix[ii,:]))
        RightParams = numpy.concatenate((RightParams,stimulusMatrix[jj,:]))
print LeftParams
print RightParams
#add in some monocular conditions
LeftParams = numpy.concatenate((LeftParams,[0,1]))
RightParams = numpy.concatenate((RightParams,[0,0]))
LeftParams = numpy.concatenate((LeftParams,[0,0]))
RightParams = numpy.concatenate((RightParams,[0,1]))

LeftParams = numpy.concatenate((LeftParams,[0,0.3]))
RightParams = numpy.concatenate((RightParams,[0,0]))
LeftParams = numpy.concatenate((LeftParams,[0,0]))
RightParams = numpy.concatenate((RightParams,[0,0.3]))

LeftParams = numpy.concatenate((LeftParams,[0,0.1]))
RightParams = numpy.concatenate((RightParams,[0,0]))
LeftParams = numpy.concatenate((LeftParams,[0,0]))
RightParams = numpy.concatenate((RightParams,[0,0.1]))


LeftParams = numpy.concatenate((LeftParams,[-.45,1]))
RightParams = numpy.concatenate((RightParams,[-.45,0]))
LeftParams = numpy.concatenate((LeftParams,[-.45,0]))
RightParams = numpy.concatenate((RightParams,[-.45,1]))

LeftParams = numpy.concatenate((LeftParams,[-.45,0.3]))
RightParams = numpy.concatenate((RightParams,[-.45,0]))
LeftParams = numpy.concatenate((LeftParams,[-.45,0]))
RightParams = numpy.concatenate((RightParams,[-.45,0.3]))

LeftParams = numpy.concatenate((LeftParams,[-.45,0.1]))
RightParams = numpy.concatenate((RightParams,[-.45,0]))
LeftParams = numpy.concatenate((LeftParams,[-.45,0]))
RightParams = numpy.concatenate((RightParams,[-.45,0.1]))


LeftParams = numpy.concatenate((LeftParams,[-.9,1]))
RightParams = numpy.concatenate((RightParams,[-.9,0]))
LeftParams = numpy.concatenate((LeftParams,[-.9,0]))
RightParams = numpy.concatenate((RightParams,[-.9,1]))

LeftParams = numpy.concatenate((LeftParams,[-.9,0.3]))
RightParams = numpy.concatenate((RightParams,[-.9,0]))
LeftParams = numpy.concatenate((LeftParams,[-.9,0]))
RightParams = numpy.concatenate((RightParams,[-.9,0.3]))

LeftParams = numpy.concatenate((LeftParams,[-.9,0.1]))
RightParams = numpy.concatenate((RightParams,[-.9,0]))
LeftParams = numpy.concatenate((LeftParams,[-.9,0]))
RightParams = numpy.concatenate((RightParams,[-.9,0.1]))

# total = 81 + 18 now (after monoc added)

RightParams = RightParams.reshape(99,2);
LeftParams = LeftParams.reshape(99,2);

stimIDs = range(99)


clock = core.Clock() # make one clock, instead of a new instance every time. Use 
for trial in range(0,numTrials):
    #determine stim order
    print "Beginning Trial",trial+1
    
    random.shuffle(stimIDs)
    
    for stimNumber in stimIDs:
        
        print stimNumber+1
        trigger.preStim(stimNumber+1)
        
        # left eye grating
        meanLuminance = LeftParams[stimNumber,0]
        luminanceRange = LeftParams[stimNumber,1]
        
        print meanLuminance, luminanceRange    
        a = meanLuminance - (1+meanLuminance)*luminanceRange;
        b = meanLuminance + (1+meanLuminance)*luminanceRange;
        textureType=numpy.array([a,b])[numpy.newaxis]
        gratingStim1 = visual.GratingStim(win=myWin,mask='None', tex=textureType,units='deg',size=[130,130], sf=spatialFreq, autoLog=False)
        gratingStim1.pos = [-67,0]
        gratingStim1.ori = 0
    
        # right eye grating
        meanLuminance = RightParams[stimNumber,0]
        luminanceRange = RightParams[stimNumber,1]
        
        print meanLuminance, luminanceRange    
        a = meanLuminance - (1+meanLuminance)*luminanceRange;
        b = meanLuminance + (1+meanLuminance)*luminanceRange;
        textureType=numpy.array([a,b])[numpy.newaxis]
        gratingStim2 = visual.GratingStim(win=myWin,mask='None', tex=textureType,units='deg',size=[130,130], sf=spatialFreq, autoLog=False)
        gratingStim2.pos = [67,0]
        gratingStim2.ori = 180
    
        gratingStim1.setAutoDraw(True)
        gratingStim2.setAutoDraw(True)
        
        changeDirectionTimeAt = stimDuration * changeDirectionAt
        clock.reset()
        while clock.getTime()<stimDuration:
            if clock.getTime()>changeDirectionTimeAt:
                gratingStim1.setPhase(0 + changeDirectionTimeAt*temporalFreq1 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq1)
                gratingStim2.setPhase(0 + changeDirectionTimeAt*temporalFreq1 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq1)
            else:
                gratingStim1.setPhase(0 + clock.getTime()*temporalFreq1)
                gratingStim2.setPhase(0 + clock.getTime()*temporalFreq1)
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






#clrctr=1;
#print "made grating"
#
#
#monocStims = 8
#binocStims = 8+2
#totalStims = monocStims+binocStims
#
#pos=[-67, 0]
#
#run
#clock = core.Clock() # make one clock, instead of a new instance every time. Use 
#print "\n",str(totalStims+doBlank), "stims will be run for",str(numTrials),"trials."
#if nBlank > 1:
#    print "Will run blank "+str(nBlank)+" times"
# # force a wait period of at least 5 seconds before first stim
#if initialDelay>0:
#    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
#    gratingStimLow.setContrast(0)
#    gratingStimHigh.setContrast(0)
#    while clock.getTime()<initialDelay:
#        myWin.flip()
#for trial in range(0,numTrials):
#    #determine stim order
#    print "Beginning Trial",trial+1
#    stimOrder = range(0,totalStims+doBlank)
#    if nBlank > 1:
#        blankID=totalStims
#        for ibl in range(1,nBlank):
#            stimOrder.append(blankID)
#    if isRandom:
#        random.shuffle(stimOrder)
#    for stimNumber in stimOrder:
#        trigger.preStim(stimNumber+1)
#        # convert orientations to standard lab notation
#        gratingStimLow.setContrast(0)
#        gratingStimHigh.setContrast(0)
#        gratingStimLow2.setAutoDraw(False)
#        gratingStimHigh2.setAutoDraw(False)
#        print stimNumber
#        
#        if stimNumber == totalStims:
#            gratingStimLow.setContrast(0)
#            gratingStimHigh.setContrast(0)
#            print "\tStim",stimNumber+1," (blank)"
#            
#            
#        #monocular conditions
#        elif stimNumber == 0:
#            #left eye high lum high cont
#            gratingStimHigh.setContrast(1)
#            gratingStimLow.pos = [67,0]
#            gratingStimHigh.pos = [-67,0]
#        elif stimNumber == 1:
#        #left eye high lum low cont
#            gratingStimHigh.setContrast(.25)
#            gratingStimLow.pos = [67,0]
#            gratingStimHigh.pos = [-67,0]
#        elif stimNumber == 2:
#        #left eye low lum high cont
#            gratingStimLow.setContrast(1)
#            gratingStimLow.pos = [-67,0]
#            gratingStimHigh.pos = [67,0]
#        elif stimNumber == 3:
#        #left eye low lum low cont
#            gratingStimLow.setContrast(.25)
#            gratingStimLow.pos = [-67,0]
#            gratingStimHigh.pos = [67,0]
#        elif stimNumber == 4:
#        #right eye high lum high cont
#            gratingStimHigh.setContrast(1)
#            gratingStimHigh.pos = [67,0]
#            gratingStimLow.pos = [-67,0]
#        elif stimNumber == 5:
#        #right eye high lum low cont
#            gratingStimHigh.setContrast(.25)
#            gratingStimHigh.pos = [67,0]
#            gratingStimLow.pos = [-67,0]
#        elif stimNumber == 6:
#        #right eye low lum high cont
#            gratingStimLow.setContrast(1)
#            gratingStimLow.pos = [67,0]
#            gratingStimHigh.pos = [-67,0]
#        elif stimNumber == 7:
#        #right eye low lum low cont
#            gratingStimLow.setContrast(.25)
#            gratingStimLow.pos = [67,0]
#            gratingStimHigh.pos = [-67,0]
#            
#        #binocular conditions
#        elif stimNumber == 8:
#            gratingStimHigh.setContrast(1)
#            gratingStimHigh.pos = [-67,0]
#            gratingStimLow.setContrast(1)
#            gratingStimLow.pos = [67,0]
#        elif stimNumber == 9:
#            gratingStimHigh.setContrast(1)
#            gratingStimHigh.pos = [-67,0]
#            gratingStimLow.setContrast(.25)
#            gratingStimLow.pos = [67,0]
#        elif stimNumber == 10:
#            gratingStimHigh.setContrast(.25)
#            gratingStimHigh.pos = [-67,0]
#            gratingStimLow.setContrast(1)
#            gratingStimLow.pos = [67,0]
#        elif stimNumber == 11:
#            gratingStimHigh.setContrast(.25)
#            gratingStimHigh.pos = [-67,0]
#            gratingStimLow.setContrast(.25)
#            gratingStimLow.pos = [67,0]
#        elif stimNumber == 12:
#            gratingStimHigh.setContrast(1)
#            gratingStimHigh.pos = [67,0]
#            gratingStimLow.setContrast(1)
#            gratingStimLow.pos = [-67,0]
#        elif stimNumber == 13:
#            gratingStimHigh.setContrast(1)
#            gratingStimHigh.pos = [67,0]
#            gratingStimLow.setContrast(.25)
#            gratingStimLow.pos = [-67,0]
#        elif stimNumber == 14:
#            gratingStimHigh.setContrast(.25)
#            gratingStimHigh.pos = [67,0]
#            gratingStimLow.setContrast(1)
#            gratingStimLow.pos = [-67,0]
#        elif stimNumber == 15:
#            gratingStimHigh.setContrast(.25)
#            gratingStimHigh.pos = [67,0]
#            gratingStimLow.setContrast(.25)
#            gratingStimLow.pos = [-67,0]
#        elif stimNumber == 16:
#            gratingStimHigh.setContrast(1)
#            gratingStimHigh.pos = [-67,0]
#            gratingStimHigh2.setContrast(1)
#            gratingStimHigh2.pos = [67,0]
#            gratingStimHigh2.setAutoDraw(True)
#        elif stimNumber == 17:
#            gratingStimLow.setContrast(1)
#            gratingStimLow.pos = [-67,0]
#            gratingStimLow2.setContrast(1)
#            gratingStimLow2.pos = [67,0]
#            gratingStimLow2.setAutoDraw(True)
#            
#        print "\tStim",stimNumber+1
#        if stimNumber==16:
#            changeDirectionTimeAt = stimDuration * changeDirectionAt
#            clock.reset()
#            while clock.getTime()<stimDuration:
#                if clock.getTime()>changeDirectionTimeAt:
#                    gratingStimHigh.setPhase(0 + changeDirectionTimeAt*temporalFreq1 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq1)
#                    gratingStimHigh2.setPhase(0 + changeDirectionTimeAt*temporalFreq2 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq2)
#                else:
#                    gratingStimHigh.setPhase(0 + clock.getTime()*temporalFreq1)
#                    gratingStimHigh2.setPhase(0 + clock.getTime()*temporalFreq2)
#                trigger.preFlip(None)
#                myWin.flip()
#                trigger.postFlip(None)
#        elif stimNumber==17:
#            changeDirectionTimeAt = stimDuration * changeDirectionAt
#            clock.reset()
#            while clock.getTime()<stimDuration:
#                if clock.getTime()>changeDirectionTimeAt:
#                    gratingStimLow.setPhase(0 + changeDirectionTimeAt*temporalFreq1 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq1)
#                    gratingStimLow2.setPhase(0 + changeDirectionTimeAt*temporalFreq2 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq2)
#                else:
#                    gratingStimLow.setPhase(0 + clock.getTime()*temporalFreq1)
#                    gratingStimLow2.setPhase(0 + clock.getTime()*temporalFreq2)
#                trigger.preFlip(None)
#                myWin.flip()
#                trigger.postFlip(None)
#        else:
#            changeDirectionTimeAt = stimDuration * changeDirectionAt
#            clock.reset()
#            while clock.getTime()<stimDuration:
#                if clock.getTime()>changeDirectionTimeAt:
#                    gratingStimLow.setPhase(0 + changeDirectionTimeAt*temporalFreq1 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq1)
#                    gratingStimHigh.setPhase(0 + changeDirectionTimeAt*temporalFreq2 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq2)
#                else:
#                    gratingStimLow.setPhase(0 + clock.getTime()*temporalFreq1)
#                    gratingStimHigh.setPhase(0 + clock.getTime()*temporalFreq2)
#                trigger.preFlip(None)
#                myWin.flip()
#                trigger.postFlip(None)
#                
#                
#        #now do ISI
#        if isi !=0:
#            clock.reset()
#            gratingStimLow.setContrast(0)
#            gratingStimLow.pos = [-67,0]
#            gratingStimHigh.setContrast(0)
#            gratingStimHigh.pos = [-67,0]
#            trigger.preFlip(None)
#            myWin.flip()
#            trigger.postFlip(None)
#            while clock.getTime()<isi:
#                #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
#                myWin.flip()
#        trigger.postStim(None)
#
#trigger.wrapUp([logFilePath, expName])
