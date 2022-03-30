
from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path

mon= monitors.Monitor('Acer') #gets the calibration
#----------distance off by 2x, 50 cm == 25 cm

isUserControlled = 0# If 1, the user can use "z" to flash the screen, 'c' to set to gray, 'x' to show a static grating

# ---------- Stimulus Parameters ---------- # 
numOrientations = 16
orientations = numpy.arange(0,360,360.0/numOrientations)#Remember, ranges in Python do NOT include the final value!
#orientations = [45,225];

numTrials =400 #Run all the stims this many times
doBlank = 0 #0 for no blank stim, 1 to have a blank stim. The blank will have the highest stimcode.

stimDuration = 1
changeDirectionAt = 1 #when do we change movement directions? If 1, there should be no reversal.
isi = 1
isRandom = 0
# Grating parameter
temporalFreq = 4
spatialFreq = .1
contrast = .925
textureType = 'sin' #'sqr' = square wave, 'sin' = sinusoidal
startingPhase=0 # initial phase for gratingStim

#aperture and position parameters
#centerPoint = [0,0]
centerPoint = [-68,0]

stimSize = [40,40] #Size of grating in degrees

#Experiment logging parameters
dataPath='x:/'
animalName='search';
logFilePath =dataPath+animalName+'\\'+animalName+'.txt' #including filepath

# ---------- Stimulus code begins here ---------- #
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#make a window
myWin = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=True)

changeDirectionTimeAt = stimDuration * changeDirectionAt

#create grating stim

textureType=numpy.array([-1,1])[numpy.newaxis]

gratingStim = visual.GratingStim(win=myWin,tex=textureType,units='deg',
    pos=centerPoint,size=stimSize, sf=spatialFreq, autoLog=False,mask='circle')
gratingStim.setAutoDraw(True)

barTexture = numpy.ones([256,256,3]);
flipStim = visual.PatchStim(win=myWin,tex=barTexture,mask='gauss',units='pix',pos=[-1920,540],size=(100,100))
flipStim.setAutoDraw(True)#up left, this is pos in y, neg in x
clrctr=1;
contrastCtr=1
myContrast=contrast;
print("made grating")
#run
clock = core.Clock() # make one clock, instead of a new instance every time. Use 
print("\n",str(len(orientations)+doBlank), "stims will be run for",str(numTrials),"trials.")

for trial in range(0,numTrials): 
    #determine stim order
    print("Beginning Trial",trial+1)
    stimOrder = range(0,len(orientations)+doBlank)
    if isRandom:
        random.shuffle(stimOrder)
    for stimNumber in stimOrder:
        #display each stim
        #display stim
        flipStim.setContrast(1)
        flipStim.setAutoDraw(True)
        # convert orientations to standard lab notation
        if stimNumber == len(orientations):
            gratingStim.setContrast(0)
            print("\tStim",stimNumber+1," (blank)")
        else:
            gratingStim.setContrast(myContrast)
            gratingStim.ori = orientations[stimNumber]-90
            print("\tStim",stimNumber+1,orientations[stimNumber],'deg')
        clock.reset()
        while clock.getTime()<stimDuration:
            if isUserControlled:
                for key in event.getKeys():
                    if key in ['c']:
                        contrastCtr=contrastCtr+1
                        if contrastCtr%2==1:
                            gratingStim.setContrast(0)
                            myContrast=0;
                        else:
                            gratingStim.setContrast(contrast)
                            myContrast=contrast
            clrctr=clrctr+1;
            if clrctr%2==1:
                flipStim.setContrast(-1)
            else:
                flipStim.setContrast(1)
            if clock.getTime()>changeDirectionTimeAt:
                gratingStim.setPhase(startingPhase+changeDirectionTimeAt*temporalFreq - (clock.getTime()-changeDirectionTimeAt)*temporalFreq)
            else:
                gratingStim.setPhase(startingPhase+clock.getTime()*temporalFreq)
            myWin.flip()
    
        gratingStim.setContrast(0)
        myWin.flip()
        
        dontGo = True
        while dontGo:
            for key in event.getKeys():
                # quit
                if key in ['escape', 'q']:
                    myWin.close()
                    # win.bits.reset()
                    core.quit()
                elif key in ['down','up','right','left']:
                    dontGo  = False
    
#cleanup
mywin.close()
core.quit()
