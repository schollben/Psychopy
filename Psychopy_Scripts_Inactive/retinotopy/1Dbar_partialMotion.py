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
animalName = 'test'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

mon= monitors.Monitor('dualmonitors')


# ---------- Stimulus Parameters ---------- #
numTrials = 8

orientation = 270
stimSize = 44
centerPoint = [-72,0] #screen about 113. deg wide and XX deg tall

barWidthOverlap = 0 #set to 1 if you want bars wider than displacement ##### make the multiplier instead of 1/0
initialDelay = 1
isRandom = 0

whitebars = 1

stimON = .2
stimOFF = .001
isi= 2
numBars = 11
#-----------------------------------------------#


 #---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)
#make a window
if whitebars==1:
    back = -1
    cont = 1
else:
    back = 1
    cont = -1
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False,rgb=[back,back,back])
#create bar and ISI textures
barTexture = numpy.ones([256,256,3]);
barWidth = stimSize/numBars
if barWidthOverlap<1:
    barSize = [barWidth,stimSize*1.5] #bar length always 1.5x size
else:
     barSize = [barWidth*1.5,stimSize*1.5] #bar length always 1.5x size, here increased bar width for 50% overlap
print barSize
barStim = visual.PatchStim(win=myWin,tex=barTexture,mask='none',units='deg',pos=centerPoint,size=barSize,ori=orientation-90)
barStim.setPos(centerPoint)
barStim.setAutoDraw(True)

#set up bar shifts
shifts = numpy.arange(0,numBars,1)
shifts = shifts-(numBars-1)/2
shifts = shifts*barWidth
stiminfo = shifts
print shifts


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
        #stimDuration = trigger.extendStimDurationToFrameEnd(stimDuration)
    # store the stimulus data and prepare the directory
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType


clock = core.Clock()
print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
barStim.setContrast(back)
while clock.getTime()<initialDelay:
    myWin.flip()

for trial in range(0,numTrials):
    #determine stim order
    print "Beginning Trial",trial+1
    
    #partial and full shifts
    # 1 full and 4 partial motion stim----- total of 5 trials!
    partialMotionNum = 5
    for n in range(0,partialMotionNum):
        
        stimOrder = range(0,len(shifts))
        
        if n==1:
            if numBars==9:
                stimOrder = range(0,3)
            if numBars==11:
                stimOrder = range(0,4)
        if n==2:
            if numBars==9:
                stimOrder = range(3,6)
            if numBars==11:
                stimOrder = range(4,7)
        if n==3:
            if numBars==9:
                stimOrder = range(6,9)
            if numBars==11:
                stimOrder = range(7,11)
        if n==4:
            if numBars==9:
                stimOrder = range(0,3)+range(6,9)
            if numBars==11:
                stimOrder = range(0,4)+range(7,11)
                
        print stimOrder
        print "right motion"
        trigger.preStim(n)
        for stimNumber in stimOrder:
            barStim.setPos([shifts[stimNumber]*math.sin(orientation*math.pi/180) + centerPoint[0] ,shifts[stimNumber]*math.cos(orientation*math.pi/180)  + centerPoint[1]])
            clock.reset()
            while clock.getTime()<stimON+stimOFF:
                if clock.getTime()< stimON:
                    barStim.setContrast(cont)
                else:
                    barStim.setContrast(back)
                trigger.preFlip(None)
                myWin.flip()
                trigger.postFlip(None)
                
        #now do ISI
        clock.reset()
        while clock.getTime()<isi:
            barStim.setContrast(back)
            myWin.flip()
           
        stimOrder.reverse()
        
        print stimOrder
        print "left motion"
        trigger.preStim(n+partialMotionNum)
        
        for stimNumber in stimOrder:
            barStim.setPos([shifts[stimNumber]*math.sin(orientation*math.pi/180) + centerPoint[0] ,shifts[stimNumber]*math.cos(orientation*math.pi/180)  + centerPoint[1]])
            clock.reset()
            while clock.getTime()<stimON+stimOFF:
                if clock.getTime()< stimON:
                    barStim.setContrast(cont)
                else:
                    barStim.setContrast(back)
                trigger.preFlip(None)
                myWin.flip()
                trigger.postFlip(None)
                
       #now do ISI
        clock.reset()
        while clock.getTime()<isi:
            barStim.setContrast(back)
            myWin.flip() 