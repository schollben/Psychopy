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
print "initialized"

#---------- Stimulus Description ---------- #
'''Flashes grid squares''' 
#---------- Monitor Properties ----------#v
mon= monitors.Monitor('projector') #gets the calibration for stimMonitor
#---------- Constants --------------#
#emissionRes = .342 # camera pixels per um at 1x1 binning
#excitationRes = .2# monitor pixels per um

#---------- Parameters----------#
nTrials=100 # runs forever!
doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=1; # number of blanks to show per trial.
stimDuration = .1 # length of time each dot appears in seconds
isi = 0 # length of inter stimulus interval in seconds
winSize=1000 # window size in pixels
spotSize  = 500# size of illumination spot in pixels->> 20 pix is ~100um
power = 1  # power of light spot, ranges from -1 to 1
initialDelay = 0 # initial delay in seconds    

boxColor = [1,1,1]
#boxColor = [-.3,-.3,-.3]
# Create window where we can draw stimuli
myWin = visual.Window(size=(winSize,winSize),pos=(0,0),monitor=mon,fullscr=True,screen=0, allowGUI=True, waitBlanking=True)
myWin.color = [-1, -1 ,-1] # make it black

# Initialize Rect stim
boxStim = visual.Rect(win=myWin, units='pix', size=spotSize, pos=(-50,0), lineColor = 'white', fillColor =boxColor,lineWidth = 1)
boxStim.setAutoDraw(True)
# create instance of clock object to use as timer
myMouse = event.Mouse(win=myWin)
increment = 25
boxStim.pos = [-50,100]

while True:    
    for key in event.getKeys():
            if key in ['up']:
                boxStim.setPos([0,increment],'+')
                print "Position = ", str(boxStim.pos)
            if key in ['down']:
                boxStim.setPos([0,increment],'-')
                print "Position = ", str(boxStim.pos)
            if key in ['left']:
                boxStim.setPos([increment,0],'-')
                print "Position = ", str(boxStim.pos)
            if key in ['right']:
                boxStim.setPos([increment,0],'+')
                print "Position = ", str(boxStim.pos)
            if key in['8']:
                boxStim.setPos([0,0])
                print "Position=", str(boxStim.pos)
            if key in ['s']:
                boxStim.setSize(25,'-')
                print "Size = ", str(boxStim.size/2)
            if key in ['x']:
                boxStim.setSize(800)
                print "Size = ", str(boxStim.size/2)
            if key in ['w']:
                boxStim.setSize(25, '+')
                print "Size = ", str(boxStim.size/2)
            if key in ['z']:
                boxStim.fillColor = [-1,-1,-1]
                
    boxStim.setContrast(power);
    myWin.flip()
    mouse_dX,mouse_dY = myMouse.getRel()
    mouse1, mouse2, mouse3 = myMouse.getPressed()
    if (mouse3):
        boxStim.setSize(mouse_dX, '+',1)
    elif (mouse1):
        boxStim.setPos([mouse_dX, mouse_dY], '+', 20)    
#    keys = event.getKeys()
#    if keys[0]=='escape':
#        print 'Done'
#        core.quit()
