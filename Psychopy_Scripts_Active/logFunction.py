from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import numpy.matlib
import sys
import os
import serial
from pathlib import Path

#logging
def logFileNameGenerator(stimarray):
    dataPath='D:\\Pyschopy\\'
    date = (time.strftime("%Y-%m-%d"))
    directory = dataPath+date
    if not os.path.exists(directory):
        os.mkdir(directory)
    logFilePath =dataPath+date+'\\'
    i = 1
    FileName = "T"+ f"{i:03}"+'.txt'
    while os.path.exists(logFilePath+FileName):
        i = i+1
        FileName = "T" + f"{i:03}"+'.txt'
    numpy.savetxt(logFilePath+FileName,stimarray)
    return logFilePath, FileName
    
def logScript(currentAddress,fileName, path, name):
    os.chdir(str(path))
    f = open(str(name + "_script.txt"), 'x')
    f = open(str(name + "_script.txt"), 'w')
    os.chdir(str(currentAddress))
    rfi = open(str(fileName), 'r')
    while True:
        l = rfi.readline()
        f.writelines(l + '\n')
        if not l :
            break
    rfi.close()
    f.close()
    

