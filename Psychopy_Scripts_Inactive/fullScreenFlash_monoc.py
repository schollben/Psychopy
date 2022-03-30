from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
from os import path
print "initialized"

# ---------- Stimulus Description ---------- #
'''A fullscreen drifting grating for 2pt orientation tuning'''
#---------- Monitor Properties ----------#
mon= monitors.Monitor('dualmonitors') #gets the calibration
mon.setDistance(26)
overwriteGammaCalibration=True
newGamma=0.479
newGamma=1

dispMonitor=-1 # 1 to show stim on right, -1 to show stim on left

initialDelay=5 # time in seconds to wait before first stimuli. Set to 0 to begin ASAP. 
lum0=0.0 # baseline and isi luminance.
lum1=1.0
contrastCounter=0
flashInterval = 5# duration lum1 is shown
isi=5
numTrials = 20#Run all the stims this many times

#Triggering type
#Can be either:
# "NoTrigger" - no triggering; stim will run freely
# "SerialDaqOut" - Triggering by serial port. Stim codes are written to the MCC DAQ.
triggerType = 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "None"
adjustDurationToMatch2P=True

#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)
orientations=''
#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)
if overwriteGammaCalibration:
    myWin.setGamma(newGamma)
    print "Overwriting Gamma Calibration. New Gamma value:",newGamma
 
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
        flashInterval = trigger.extendStimDurationToFrameEnd(flashInterval)
    # store the stimulus data and prepare the directory
    trigger.preTrialLogging([dataPath,date,expName,stimCodeName,orientations,logFilePath])
elif triggerType=="DaqIntrinsicTrigger":
    import daqIntrinsicTrigger
    trigger = daqIntrinsicTrigger.daqIntrinsicTrigger(None) 
else:
    print "Unknown trigger type", triggerType
        
print flashInterval

stim = visual.PatchStim(myWin, units='deg',tex="sqrXsqr",texRes=64,
    size=[135,135], sf=.0008, mask = 'none', pos=(dispMonitor*67,0))
stim.setAutoDraw(True)
stim.setColor(lum0*255, 'rgb255')

stim2 = visual.PatchStim(myWin, units='deg',tex="sqrXsqr",texRes=64,
    size=[135,135], sf=.0008, mask = 'none', pos=(-1*dispMonitor*67,0))
stim2.setAutoDraw(True)
stim2.setColor(lum0*255, 'rgb255')
stim2.setContrast(1)

clock=core.Clock()
if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to acquire a baseline."
    stim.setContrast(1)
    while clock.getTime()<initialDelay:
        myWin.flip()

clock.reset()
for trial in range(0,numTrials): 
    print "Beginning Trial",trial+1
    stim.setContrast(1)
    stim.setColor(lum1*255, 'rgb255')
    trigger.preStim(1)
    clock.reset()
    while clock.getTime()<flashInterval:
        trigger.preFlip(None)
        myWin.flip()
        trigger.postFlip(None)    
    stim.setColor(lum0*255, 'rgb255')
    clock.reset()
    myWin.flip()
    trigger.preStim(0)
    ff=True
    while clock.getTime()<isi: # this is the isi
        #print "isi ",isi," clock ",clock.getTime()
        if ff:
            trigger.preFlip(None)
        myWin.flip() 
        if ff:
            trigger.postFlip(None)
            ff=False
    trigger.postStim(None)
    
trigger.wrapUp([logFilePath, expName])
print 'Finished all stimuli.'