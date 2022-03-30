
from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
from os import path
print "initialized"

mon= monitors.Monitor('dualmonitors') #gets the calibration
#----------distance off by 2x, 50 cm == 25 cm

isUserControlled = 0# If 1, the user can use "z" to flash the screen, 'c' to set to gray, 'x' to show a static grating

# ---------- Stimulus Parameters ---------- # 
numOrientations = 16
orientations = numpy.arange(0,180,180.0/numOrientations) #Remember, ranges in Python do NOT include the final value!
#orientations = [110,120,130,140, 150];

numTrials =400 #Run all the stims this many times
doBlank = 0 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.

stimDuration = 1
changeDirectionAt = 1 #when do we change movement directions? If 1, there should be no reversal.
isi = 1
isRandom = 0 
# Grating parameter
temporalFreq = 4
spatialFreq = 0.25
contrast = .99
textureType = 'sin' #'sqr' = square wave, 'sin' = sinusoidal
startingPhase=0 # initial phase for gratingStim

#aperture and position parameters
#centerPoint = [0,0]
centerPoint = [-63,0]
#centerPoint = [63,0]

stimSize = [800, 800] #Size of grating in degrees

#Triggering type
#Can be any of:
# "NoTrigger" - no triggering; stim will run freely
# "SerialDaqOut" - Triggering by serial port. Stim codes are written to the MCC DAQ.
# "OutOnly" - no input trigger, but does all output (to CED) and logging
#triggerType ='SerialDaqOut'
triggerType = 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "None"
adjustDurationToMatch2P=True

#Experiment logging parameters
dataPath='x:/'
animalName='search';
logFilePath =dataPath+animalName+'\\'+animalName+'.txt' #including filepath

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
    trigger = serialTriggerDaqOut.serialTriggerDaqOut(serialPortName) 
    if triggerType == 'OutOnly':
        trigger.readSer=False
    #Record a bunch of serial triggers and fit the stim duration to an exact multiple of the trigger time
    if adjustDurationToMatch2P:
        stimDuration = trigger.extendStimDurationToFrameEnd(stimDuration)
    # determine the Next experiment file name
    expName=trigger.getNextExpName([dataPath,animalName])
    # store the stimulus data and prepare the directory
    #trigger.preTrialLogging([dataPath,animalName,expName,stimCodeName,orientations])
else:
    print "Unknown trigger type", triggerType
        
print stimDuration
changeDirectionTimeAt = stimDuration * changeDirectionAt

#create grating stim

textureType=numpy.array([-1,1])[numpy.newaxis]

gratingStim = visual.GratingStim(win=myWin,tex=textureType,units='deg',
    pos=centerPoint,size=stimSize, sf=spatialFreq, autoLog=False,mask='none')
gratingStim.setAutoDraw(True)

barTexture = numpy.ones([256,256,3]);
flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='gauss',units='pix',pos=[-1920,540],size=(100,100))
flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x
clrctr=1;
contrastCtr=1
myContrast=contrast;
print "made grating"
#run
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
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
            gratingStim.setContrast(myContrast)
            gratingStim.ori = orientations[stimNumber]-90
            print "\tStim",stimNumber+1,orientations[stimNumber],'deg'
        clock.reset()
        while clock.getTime()<stimDuration:
            if isUserControlled:
                for key in event.getKeys():
                    if key in ['c']:
                        contrastCtr=contrastCtr+1
                        if contrastCtr%2==1:
                            gratingStim.setContrast(0)
                            myContrast=0;
                        else:
                            gratingStim.setContrast(contrast)
                            myContrast=contrast
            clrctr=clrctr+1;
            if clrctr%2==1:
                #flipStim.setColor((0,0,0),colorSpace='rgb')
                flipStim.setContrast(-1)
            else:
                #flipStim.setColor((1,1,1),colorSpace='rgb')
                flipStim.setContrast(1)
            if clock.getTime()>changeDirectionTimeAt:
                gratingStim.setPhase(startingPhase+changeDirectionTimeAt*temporalFreq - (clock.getTime()-changeDirectionTimeAt)*temporalFreq)
            else:
                gratingStim.setPhase(startingPhase+clock.getTime()*temporalFreq)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
            
        #now do ISI
        clock.reset()
        gratingStim.setContrast(0)
        flipStim.setContrast(0)
        #print 'isi'
        trigger.preFlip(None)
        myWin.flip()
        trigger.postFlip(None)
        flipStim.setAutoDraw(False)
        while clock.getTime()<isi:
            #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
            myWin.flip()
            if isUserControlled:
                for key in event.getKeys():
                    if key in ['c']:
                        contrastCtr=contrastCtr+1
                        if contrastCtr%2==1:
                            myContrast=0;
                        else:
                            myContrast=contrast
        trigger.postStim(None)

#trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'