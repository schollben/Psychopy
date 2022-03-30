from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
from os import path
print "initialized"

#Triggering type
triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly' OR 'NoTrigger'
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True

#Experiment logging parameters
#--------#
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath
#--------#

#---------- Monitor Properties ----------#
mon= monitors.Monitor('dualmonitors') #gets the calibration





# ---------- Stimulus Parameters ---------- #
#trials and duration
numDirections = 4 #typically 4, 8, or 16# 
directions = numpy.arange(0,360,360.0/numDirections) #Remember, ranges in Python do NOT include the final value!
numTrials=6#Run all the stims this many times
doBlank = 0#0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=1; # number of blanks to show per trial.
stimDuration =1.0
isi = 2
isRandom =1
initialDelay=0# time in seconds to wait before first stimuli. Set to 0 to begin ASAP. 

# RDK parameters
backgroundColor = 1.0; #-1.0 is black, 0.0 is gray, and 1.0 is white
stimColor = -1.0; #-1.0 is black, 0.0 is gray, and 1.0 is white
temporalFreq = 0.02;
numberOfDots = 2000/12;
stimCoherence = 1;
sizeOfDots = 10; 
#aperture and position parameters 
centerPoint = [0,0] 
stimSize = [300,300] #Size of RDK in degrees


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
    stiminfo = 0
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath]) 
    #--------#
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
        
print stimDuration

# create RDK stim (must be done each stimulus presentation due to the direction of the stim not changing whenver the dir variable is changed
rdkStim = visual.DotStim(win=myWin, units='pix', nDots=numberOfDots/2, coherence=stimCoherence, fieldPos=centerPoint, fieldSize=stimSize, 
    fieldShape='sqr', dotSize=sizeOfDots, dotLife=10, dir = 0.0, speed=temporalFreq, color=(stimColor, stimColor, stimColor), 
    colorSpace='rgb', opacity=1.0, contrast=1.0, signalDots='same', noiseDots='direction',autoLog=False);
rdkStim2 = visual.DotStim(win=myWin, units='pix', nDots=numberOfDots/2, coherence=stimCoherence, fieldPos=centerPoint, fieldSize=stimSize, 
    fieldShape='sqr', dotSize=sizeOfDots, dotLife=100, dir = 0.0, speed=temporalFreq, color=(1, 1, 1), 
    colorSpace='rgb', opacity=1.0, contrast=1.0, signalDots='same', noiseDots='direction',autoLog=False);
rdkStim.setAutoDraw(True)
rdkStim2.setAutoDraw(True)

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
    
    numBlocks = 8*4   #retinotopic grid 6x3 = 320x320 pixels on each screen
    # now doing 8 x 4 grid 240 x 240 pixels on each screen
    
    allBlocks = range(1,numBlocks+1+doBlank)
    random.shuffle(allBlocks)
    print allBlocks
    for block in allBlocks:
        #display each stim
        trigger.preStim(block)
        if block==numBlocks+1 and doBlank==1:
            rdkStim.setContrast(0)
            rdkStim2.setContrast(0)
        else:
            rdkStim.setContrast(1)
            rdkStim2.setContrast(1)
        if block<9:
            position = [-1920+(240/2)+240*(block-1) , 270/2 + 270]
        elif block>8 and block<17:
            position = [-1920+(240/2)+240*(block-1-8) , 270/2]
        elif block>16 and block<25:
            position = [-1920+(240/2)+240*(block-1-16) ,-270/2]
        else:
            position = [-1920+(240/2)+240*(block-1-24) , -270/2 - 240]
        print str(position)
        rdkStim.fieldPos = position
        rdkStim2.fieldPos = position
        #display stim
        for stimNumber in range(0,len(directions)):
            print "\tBlock",block," Orientation",directions[stimNumber]
            rdkStim.setDir(directions[stimNumber]-90)
            rdkStim2.setDir(directions[stimNumber]-90)
            clock.reset()
            oriDur=stimDuration/len(directions)
            while clock.getTime()<oriDur:
                trigger.preFlip(None)   
                myWin.flip()
                trigger.postFlip(None)
            
        #now do ISI
        if isi !=0:
            clock.reset()
            trigger.preFlip(None)
            rdkStim.setContrast(0)
            rdkStim2.setContrast(0)
            myWin.flip()
            trigger.postFlip(None)
            while clock.getTime()<isi:
                #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
                myWin.flip()
        trigger.postStim(None)

trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'