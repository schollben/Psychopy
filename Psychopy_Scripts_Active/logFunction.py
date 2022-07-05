from psychopy import visual, logging, core, event, monitors
from psychopy.visual import filters
import pylab, math, random, numpy, time, imp
import numpy.matlib
import sys
import os
import serial
from pathlib import Path

#logging
def logFileNameGenerator(stem):
    dataPath='D:\\Pyschopy\\'
    date = (time.strftime("%Y-%m-%d"))
    directory = dataPath+date
    if not os.path.exists(directory):
        os.mkdir(directory)
    logFilePath =dataPath+date+'\\'
    #+'\\'+Path(__file__).stem #filepath
    i = 1
    FileName = str(stem)+ f"{i:03}"+'.txt'
    #os.chdir(str(logFilePath))
    while os.path.exists(logFilePath+FileName):
        i = i+1
        FileName = str(stem) + f"{i:03}"+'.txt'
    #print(logFilePath+FileName) #new file name and location
    #numpy.savetxt(logFilePath+FileName,data)
    return logFilePath, FileName
    
def logScript(stem, fileName, path, name):
    os.chdir(str(path))
    f = open(str(name + "_script.txt"), 'x')
    f = open(str(name + "_script.txt"), 'w')
    os.chdir('C:\\Users\\scholab\\Documents\\Psychopy\\Psychopy_Scripts_Active')
    rfi = open(str(fileName), 'r')
    while True:
        l = rfi.readline()
        f.writelines(l + '\n')
        if not l :
            break
    rfi.close()
    f.close()
    

