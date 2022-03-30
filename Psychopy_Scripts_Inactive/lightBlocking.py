
from psychopy import visual, core, event, misc, logging, gui, monitors
import csv, pylab, math, random, numpy, time, imp, sys

myWin = visual.Window(monitor='dualmonitors',
    size=(3840,1080), 
    fullscr=True,
    allowGUI = False,
    screen=1,
    units = 'deg')
contrastCounter=0
flashInterval = 4       # interval for autonomous flashing
isUserControlled = 1  # If 1, the user can use "z" to flash the screen, 'c' to set to gray, 'x' to show a static grating


#stim = visual.PatchStim(myWin, tex="sqrXsqr",texRes=4,
#          size=[500,500], sf=.0005, mask = 'none', pos=(1,1))
          
stim = visual.PatchStim(myWin, tex="sqrXsqr",texRes=64,
    size=[500,500], sf=.0008, mask = 'none', pos=(1,1))
stim.setAutoDraw(True)
gratingStim = visual.GratingStim(win=myWin,tex='sin',units='deg',
    pos=[0,0],size=[300,300], sf=0.06, autoLog=False)
gratingStim.setAutoDraw(False)
          
if isUserControlled:
    while True:
        for key in event.getKeys():
            if key in ['z']:
                contrastCounter=contrastCounter+1
                gratingStim.setAutoDraw(False)
                if contrastCounter%2==0:
                    stim.setColor(255, 'rgb255')
                else:
                    stim.setColor(0, 'rgb255')
            if key in ['c']:
                stim.setColor(128, 'rgb255')
                gratingStim.setAutoDraw(False)
            if key in ['x']:
                gratingStim.setAutoDraw(True)
        stim.draw()
        myWin.flip()
        
else:
    while True:
        for key in event.getKeys():
            if key in ['z']:
                contrastCounter=contrastCounter+1
                if contrastCounter%2==0:
                    stim.setAutoDraw(True)
                else:
                    stim.setAutoDraw(False)
            if key in ['escape']:
                core.quit()
        clock = core.Clock()
        event.clearEvents()#get rid of other, unprocessed events
        while clock.getTime()<flashInterval:
            #stim.draw()
            myWin.flip() 
        else: 
            stim.setContrast(-1,'*')
            #stim.draw()
            myWin.flip()
            clock.reset() 