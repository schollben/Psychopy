from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import numpy.matlib
import sys
import os
import serial
from pathlib import Path

totalNumStim = 10
nCells = 1
isRandom = 1

stimOrder = numpy.arange(0,totalNumStim)
if isRandom:
    random.shuffle(stimOrder)
for n in range(0,nCells):
    addStimOrder = numpy.arange(0,totalNumStim)
    if isRandom:
        random.shuffle(addStimOrder)
    stimOrder = numpy.append(stimOrder,addStimOrder)
    
    
os.system('pause')

for k in range(0,2):
    
    for n in range(0, 1 + 1): #dont forget nonphotostim trials
        
        if n==0:
            print('nostim')
        else:
            print('stim')