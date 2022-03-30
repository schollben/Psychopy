from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, time, imp
import psychopy.visual
import psychopy.event
import sys
import os
import serial

deviceName = "/dev/ttyUSB0"
ser = serial.Serial(deviceName, 38400, timeout=1)

win = psychopy.visual.Window([1920,1080],monitor="acer240", units="pix",screen = 1)

flipStim1 = line1 = psychopy.visual.Line(win=win, units="pix", lineColor=[-1, -1, -1], lineWidth=100)
line1.start = [-960, -540], line1.end = [0, 540]
line2 = psychopy.visual.Line(win=win, units="pix", lineColor=[1, 1, 1], lineWidth = 100), 
line2.start = [500, -540], line2.end = [500, 540]
flipStim1.setAutoDraw(True)

flipStim1 = line1 = psychopy.visual.Line(win=win, units="pix", lineColor=[-1, -1, -1], lineWidth=100), 
line1.start = [-860, -540], line1.end = [0, 540]
line2 = psychopy.visual.Line(win=win, units="pix", lineColor=[1, 1, 1], lineWidth = 100), 
line2.start = [400, -540], line2.end = [500, 540]
flipStim1.setAutoDraw(True)

win.flip()

clock = core.Clock() 
cnt = 0
while clock.getTime()<10:
    
    currentTime = clock.getTime() 
    #print(currentTime)
    
    flipStim1.setAutoDraw(True)
    ser.setDTR(True)
    while clock.getTime() < currentTime+ 0.010:
        myWin.flip()
    ser.setDTR(False)
    flipStim1.setAutoDraw(False)
    
    flipStim2.setAutoDraw(True)
    ser.setRTS(True)
    while clock.getTime() < currentTime+ 0.020:
        myWin.flip()
    ser.setRTS(False)
    flipStim2.setAutoDraw(False)
    
ser.close()