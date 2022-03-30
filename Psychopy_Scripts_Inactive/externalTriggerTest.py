import serial, csv, time, math, datetime
from psychopy import core
import sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") 
import UniversalLibrary as UL
from abstractTrigger import trigger
from os import path,makedirs
import shutil
import glob

boardNum = 1 
baseState = 1
UL.cbDConfigPort(boardNum, UL.FIRSTPORTA, UL.DIGITALOUT)

clock = core.Clock()
print("Beginning test")
while clock.getTime()<1000:
    UL.cbDOut(boardNum,UL.FIRSTPORTA,1) 
    print clock.getTime()
    time.sleep(2)
    UL.cbDOut(boardNum,UL.FIRSTPORTA,0)
    print clock.getTime()
    time.sleep(2)
