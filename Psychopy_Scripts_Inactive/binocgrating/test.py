from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
from pedestal_grating import PedestalGratingStim

print "initialized"

# ---------- Stimulus Description ---------- #
# A fullscreen drifting grating for 2pt orientation tuning
#---------- Monitor Properties ----------#

#Triggering type
triggerType = 'OutOnly' # 'SerialDaqOut' OR 'OutOnly'
serialPortName = 'COM2' # ignored if triggerType is "COM3"
adjustDurationToMatch2P=True

#Experiment logging parameters
import time
dataPath='//mpfiwdtfitz68/Spike2Data/'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath

mon= monitors.Monitor('dualmonitors') #gets the calibration

#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)

# ---------- Stimulus Parameters ---------- #
orientations = 90
stiminfo = orientations

numTrials= 6 #Run all the stims this many times

doBlank = 1 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.
nBlank=1 # number of blanks to show per trial.
changeDirectionAt = 0.5#When do we change movement directions? If 1, there should be no reversal. Setting to 0 causes instantaneous reversal, effectively inverting all stimIDs and angles.
stimDuration =3
isi =3
isRandom =1
initialDelay=1

# Grating parameter
temporalFreq1 = 4
temporalFreq2 = 6
spatialFreq = 0.12


meanLuminance = -.5; # max value is 0 (gray)
luminanceRange = 1.0; # max value 1 (full range)

trials = range(0,10)

clock = core.Clock() # make one clock, instead of a new instance every time. Use 

changeDirectionTimeAt = stimDuration * changeDirectionAt
for n in trials:
    
    print n
    
    a = meanLuminance - (1+meanLuminance)*luminanceRange;
    b = meanLuminance + (1+meanLuminance)*luminanceRange;
    print a
    print b
    textureType=numpy.array([a,b])[numpy.newaxis]
    gratingStim = visual.GratingStim(win=myWin,mask='None', tex=textureType,units='deg',size=[130,130], sf=spatialFreq, autoLog=False)
    gratingStim.ori = 0
    gratingStim.pos = [67,0]
    gratingStim.setAutoDraw(True)
    
    
    clock.reset()
    while clock.getTime()<stimDuration:
        if clock.getTime()>changeDirectionTimeAt:
            gratingStim.setPhase(0 + changeDirectionTimeAt*temporalFreq1 - (clock.getTime()-changeDirectionTimeAt)*temporalFreq1)
        else:
            gratingStim.setPhase(0 + clock.getTime()*temporalFreq1)
        myWin.flip()
        
    clock.reset()
    gratingStim.setContrast(0)
    while clock.getTime()<stimDuration:
        myWin.flip()



