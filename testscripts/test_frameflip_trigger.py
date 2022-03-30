from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import sys
import os
import serial

#grating parameters


#initialize
deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1)

myWin = visual.Window([1920,1080],monitor="ACER", units="deg",screen = 1)

barTexture = numpy.ones([256,256,3]);

flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='none',units='deg',pos=[0,0],size=(10,10))
#flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x

flipStim1 = visual.GratingStim(win=myWin,units='deg',  ori= 0, pos=[0,0],size=(10,10), sf=1, autoLog=False,mask='circle')
flipStim1.setAutoDraw(True)

flipStim2 = visual.GratingStim(win=myWin,units='deg', ori = 90 ,pos=[0,0],size=(10,10), sf=1, autoLog=False,mask='circle')
flipStim2.setAutoDraw(True)

clock = core.Clock() 
cnt = 0
while clock.getTime()<5:
    
    currentTime = clock.getTime() 
    print(currentTime)
    
    flipStim1.setAutoDraw(True)
    ser.setDTR(True)
    ser.setDTR(False)
    myWin.flip()
    flipStim1.setAutoDraw(False)
    
    flipStim2.setAutoDraw(True)
    ser.setRTS(True)
    ser.setRTS(False)
    myWin.flip()
    flipStim2.setAutoDraw(False)
    
ser.close()
