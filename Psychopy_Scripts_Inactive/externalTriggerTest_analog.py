import serial, csv, time, math, datetime
from psychopy import core, event
from os import path,makedirs
import shutil
import glob
import numpy as np
import sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
import UniversalLibrary as UL
from abstractTrigger import trigger

boardNum = 1
baseState = 0
clock = core.Clock()
gain =  UL.UNI4VOLTS
EngUnits = 1
dataValue = UL.cbFromEngUnits(boardNum, gain, EngUnits, 0)
rampTime = 1
sleepTime = 1
trainTime =  core.Clock()
powerValues = [0.05, 0.1, 0.15, 0.2, 0.25,0.3, .4, .5, .75, 1]
print dataValue
print("Beginning test")
for maxPower in powerValues:
    print maxPower
    while trainTime.getTime()<rampTime:
        dataValue = UL.cbFromEngUnits(boardNum, gain, 4.096*maxPower*trainTime.getTime()/rampTime, 0)
        UL.cbAOut(boardNum,0,gain,dataValue) 
    time.sleep(1)
    dataValue = UL.cbFromEngUnits(boardNum, gain, 4.096*maxPower, 0)
    UL.cbAOut(boardNum,0,gain,0) 
    time.sleep(sleepTime)
    trainTime.reset()
    UL.cbAOut(boardNum,0,gain,0)

