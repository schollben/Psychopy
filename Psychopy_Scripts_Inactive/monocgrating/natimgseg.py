from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path,makedirs
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes

mon= monitors.Monitor('dualmonitors') 
clock = core.Clock() 

myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, useFBO = 'true',allowGUI=False, waitBlanking=False,blendMode='add')
#myWin.setGamma(.75) #hardcoded

stimSize = 80
SF = 0.1
TF = 4
stimPos = [-60,-5]

#imgPos = [-480,-120] 
imgPos = [-920,0]
#imgPos = [-640,0]

numTrials = 8
numTrials = range(0,numTrials);

#set up natural image display
image = visual.ImageStim(win=myWin, name='image',units='pix', pos=imgPos, size=[1000,1000])

fullConditions = 28; #28 nat images (starting from 0)

#collect full stimulus set
stimSet = numpy.asarray(range(0,fullConditions))
#random.shuffle(stimSet)
stiminfo = stimSet.flatten()
stimDuration = 2


#set up spike2 triggers
#Triggering type
triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly' OR 'NoTrigger'

serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

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
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath]) 
    #--------#
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
    

for n in numTrials:
    
    print('trial'+str(n))
    
    for nStim in stimSet:
        
        print nStim+1
        trigger.preStim(nStim+1)
        
        #load natural image to display
        nImg = nStim+1;
        
        Iname='C:/Users/fitzlab1/Desktop\psychopy/plaid/Gorris_Selected_NatImages/im' + '{:03.0f}'.format(nImg)+ '.tif'
        print Iname
        image.setAutoDraw(True)
        clock.reset()
        while clock.getTime() < 1:
            image.setImage(Iname)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
        else:
            image.setAutoDraw(False)
            while clock.getTime() < 2:
                myWin.flip()
        trigger.postStim(None)

trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'
