from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import sys
import os
import serial

deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1)
 
mon= monitors.Monitor("Acer")
myWin = visual.Window([1920,1080],monitor=mon, units="deg",screen = 1)
#thisGamma = 1.6 #human calibrated with gammaMotionNull - only works in duplication display mode?
#myWin.gamma = [thisGamma, thisGamma, thisGamma]

barTexture = numpy.ones([256,256,3]);
flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='none',units='deg',pos=[0,10],size=(10,10))
flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x

flipStim2 = visual.PatchStim(win=myWin,tex=barTexture,mask='none',units='deg',pos=[0,-10],size=(10,10))
flipStim2.setAutoDraw(True)#up left, this is pos in y, neg in x


frame_rate = myWin.getActualFrameRate(nIdentical=60, nMaxFrames=100,nWarmUpFrames=10, threshold=10)
print(frame_rate)

while True:
    ser.setRTS(True)
    ser.setRTS(False) 
    flipStim.setContrast(1)
    flipStim2.setContrast(-1)
    myWin.flip()
    ser.setRTS(True)
    ser.setRTS(False) 
    
    if len(event.getKeys())>0:
        break
    event.clearEvents()
    
ser.close()


