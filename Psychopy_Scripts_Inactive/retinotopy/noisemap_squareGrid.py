# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 09:56:05 2016

@author: wilsond
"""
from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, time, imp, sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
import numpy as np
from os import path
import matplotlib.pyplot as plt
print "initialized"
np.set_printoptions(threshold='nan')
#---------- Stimulus Description ---------- #
'''Flashes grid squares''' 
#---------- Monitor Properties ----------#v
mon= monitors.Monitor('projector') #gets the calibration for stimMonitor
#---------- Constants --------------#
#emissionRes = .342 # camera pixels per um at 1x1 binning
#excitationRes = .2# monitor pixels per um

#---------- Parameters----------#
nTrials = 20
stimDuration = .2    # length of time each dot appears in seconds
isi =0 # length of inter stimulus interval in seconds
winSize =250# window size in pixels
spotSize  =100   # size of illumination spot in pixels->> 20 pix is ~100um FWHM-------- 25px = 100 um (2017-02)
power = 1  # power of light spot, ranges from -1 to 1
res = 25 #sampling resolution, pixels between each sample
initialDelay =0# initial delay in seconds    
isRandom = 1

isCalibration = 0 # flag to do calibration after recording

xOffset =50
yOffset = -50


if isCalibration:
    nTrials = 1
    isRandom = 0
    stimDuration = .2
    isi = .2

#---------- Stimulus setup ----------#
xpos = np.tile(np.linspace(-winSize/2,winSize/2,winSize/res),[winSize/res,1])

ypos = np.transpose(np.tile(np.linspace(-winSize/2,winSize/2,winSize/res),[winSize/res,1]))



nStims = (winSize/res)**2
stimOrder = np.empty([nTrials,nStims])
for i in range(0,nTrials):
    stimOrder[i,:] = np.arange(nStims)
    if isRandom:
        random.shuffle(stimOrder[i,:])
    #print stimOrder[i,:]
    
stimOrder = stimOrder.astype(int)
stiminfo = stimOrder.flatten()
#print stiminfo
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=False

#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath
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



colorWhite=[.2,.2,.2]
 #Create window where we can draw stimuli
myWin = visual.Window(size=(1024,768),pos=(0,0),monitor=mon,fullscr=True,screen=2, allowGUI=True, waitBlanking=True)
myWin.color = [-1, -1 ,-1] # make it black
 #Initialize Rect stim
boxStim = visual.Rect(win=myWin, units='pix', size=spotSize, pos=(0,0), lineColor = 'white', fillColor = 'white')
boxStim.setAutoDraw(True)
 #create instance of clock object to use as timer
clock = core.Clock()

if initialDelay>0:
    print" waiting "+str(initialDelay)+ " seconds before starting stim to let system relax after flash"
    boxStim.setContrast(0)
    while clock.getTime()<initialDelay:
        myWin.flip()
nStims = (res)**2

for j in range(0,nTrials):
    if initialDelay>0:
        print" waiting "+str(initialDelay)+ " seconds before starting stim to let system relax after flash"
        boxStim.setContrast(0)
    while clock.getTime()<initialDelay:
        myWin.flip()
    print stimOrder[j,:]
    print j
    for i in stimOrder[j,:]:
        #print i
        trigger.preStim(i+1)
        clock.reset()
        boxStim.fillColor = [1,1,1]
        boxStim.lineColor = [1,1,1]
        boxStim.pos = (xpos[np.unravel_index(i,[winSize/res,winSize/res])]+xOffset,ypos[np.unravel_index(i,[winSize/res,winSize/res])]+yOffset)
        #print boxStim.pos
        while clock.getTime()<stimDuration:
            boxStim.contrast= power;
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
        if isi !=0:
            clock.reset()
            boxStim.setContrast(-1)
            trigger.preFlip(None)
            myWin.flip()
            trigger.postFlip(None)
            while clock.getTime()<isi:
                #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
                myWin.flip()
            trigger.postStim(None)
