import serial, csv, time, math, datetime
from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") 
import UniversalLibrary as UL
from abstractTrigger import trigger
from os import path,makedirs
import shutil
import glob

print "initialized"

# ---------- Stimulus Description ---------- #
triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True

# ---------- Set up daq ---------- #
boardNum = 1
UL.cbDConfigPort(boardNum, UL.FIRSTPORTA, UL.DIGITALOUT)
boardStateLast = 0

#Experiment logging parameters 
import time 
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

mon= monitors.Monitor('dualmonitors') #gets the calibration

myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)

radius = filters.makeRadialMatrix(256)

annulus = numpy.where(radius<1.0,1,0)*numpy.where(radius>0.5,1,0)*2 - 1

stim = visual.PatchStim(myWin,mask = annulus, pos = [-1080,0])
stim.setAutoDraw(True)

clock = core.Clock() # make one clock, instead of a new instance every time. Use 

clock.reset()
while clock.getTime()<2:
    #Keep flipping during the ISI. If you don't do this you can get weird flash artifacts when you resume flipping later.            
    myWin.flip()