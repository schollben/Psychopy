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

orientation =125
stimSize = 36
centerPoint = [-67,0]#screen about 113. deg wide and XX deg tall


barWidthOverlap = 0 #set to 1 if you want bars wider than displacement ##### make the multiplier instead of 1/0
initialDelay = 1
isRandom = 0

stimON = .25
#stimOFF = .25
stimOFFTimes = [.0001,0.05,0.25]
isi= 4
numBars = 9
#-----------------------------------------------#


 #---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)
#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False,rgb=[-1,-1,-1])
#create bar and ISI textures
barTexture = numpy.ones([256,256,3]);
barWidth = stimSize/numBars
if barWidthOverlap<1:
    barSize = [barWidth,stimSize*2] #bar length always 1.5x size
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
barStim.setContrast(-1)
while clock.getTime()<initialDelay:
    myWin.flip()

for trial in range(0,numTrials):
     stimOFForder = range(0,len(stimOFFTimes))
     print stimOFForder
     for n in stimOFForder:
         stimOFF = stimOFFTimes[n]
         #determine stim order
         print "Beginning Trial",trial+1
         stimOrder = range(0,len(shifts))
         print stimOrder
         print "right motion"
         trigger.preStim(1+n)
         print(1+n)
         
         for stimNumber in stimOrder:
             barStim.setPos([shifts[stimNumber]*math.sin(orientation*math.pi/180) + centerPoint[0] ,shifts[stimNumber]*math.cos(orientation*math.pi/180)  + centerPoint[1]])
             clock.reset()
             while clock.getTime()<stimON+stimOFF:
                 if clock.getTime()< stimON:
                     barStim.setContrast(1)
                 else:
                     barStim.setContrast(-1)
                 trigger.preFlip(None)
                 myWin.flip()
                 trigger.postFlip(None)
                
         #now do ISI
         clock.reset()
         while clock.getTime()<isi:
             barStim.setContrast(-1)
             myWin.flip()
           
         stimOrder.reverse()
         print stimOrder
         print "left motion"
         trigger.preStim(n+1+len(stimOFFTimes))
         print(n+1+len(stimOFFTimes))
        
         for stimNumber in stimOrder:
             barStim.setPos([shifts[stimNumber]*math.sin(orientation*math.pi/180) + centerPoint[0] ,shifts[stimNumber]*math.cos(orientation*math.pi/180)  + centerPoint[1]])
             clock.reset()
             while clock.getTime()<stimON+stimOFF:
                 if clock.getTime()< stimON:
                     barStim.setContrast(0)
                 else:
                     barStim.setContrast(-1)
                 trigger.preFlip(None)
                 myWin.flip()
                 trigger.postFlip(None)
                
        #now do ISI
         clock.reset()
         while clock.getTime()<isi:
             barStim.setContrast(-1)
             myWin.flip() 