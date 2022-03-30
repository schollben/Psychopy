from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes

#Experiment logging parameters
import time, os
dataPath='//mpfiwdtfitz68/Spike2Data/'
if  os.path.isdir(dataPath):
    print 'found path'
date = (time.strftime("%Y-%m-%d"))
logFilePath =dataPath+date+'\\'+date+'.txt' #including filepath
stiminfo="No data- just setting up Spike2 data files"
stimCodeName=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)

#Set up the trigger behavior
import serialTriggerDaqOut
print 'Imported trigger serialTriggerDaqOut'
trigger = serialTriggerDaqOut.serialTriggerDaqOut('COM2' ) 
# determine the Next experiment file name
expName='t00001'
print "Trial name: ",expName
# store the stimulus data and prepare the directory
trigger.preTrialLogging([dataPath,date,expName,stimCodeName,stiminfo,logFilePath])

