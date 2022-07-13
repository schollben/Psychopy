from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, time, imp
import psychopy.visual
import psychopy.event
import sys
import os
import serial

deviceName = "COM3"
ser = serial.Serial(deviceName, 38400, timeout=1)

win = psychopy.visual.Window([1920,1080],monitor="Acer", units="pix",screen = 1)

line1 = psychopy.visual.Line(win=win, units="pix", lineColor=[-1, -1, -1], lineWidth = 100)
line1.start = [-960, -540]
line1.end = [0, 540]

line2 = psychopy.visual.Line(win=win, units="pix", lineColor=[1, 1, 1], lineWidth = 100)
line2.start = [500, -540]
line2.end = [500, 540]

line1.setAutoDraw(True)
line2.setAutoDraw(True)

win.flip()

clock = core.Clock() 
cnt = 0
clock.reset()
while clock.getTime()<2:
    t1 = clock.getTime();
    #ser.setRTS(True)
    win.flip()
    #ser.setRTS(False)
    t2 = clock.getTime();
    print(1 / (t2-t1))
