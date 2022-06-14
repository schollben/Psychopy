import random, numpy, time, os
from pathlib import Path

# setting parameters
"""
cont = random.random()
size = random.random()
spatialfreq = random.random() * numpy.pi
ornt = random.random() * pi
phase = random.random()
"""

def contgenerator():
    randomcont = -2
    while randomcont > 1.5 or randomcont < -1.5 :
        randomcont = random.lognormvariate(0 , 1)
    return randomcont
    
def sizegenerator():
    randomsize = random.lognormvariate(1, 1)
    return randomsize
    
def spatialfreqgenerator():
    randomfreq = random.random() * numpy.pi * 2
    return randomfreq

def orntgenerator():
    randomornt = random.random() * numpy.pi * 2
    return randomornt
    
def phasegenerator():
    randomphase = random.lognormvariate(0, 1)
    return randomphase

def randomgenerator():
    return contgenerator(), sizegenerator(), spatialfreqgenerator(), orntgenerator(), phasegenerator()
    
#assigning values
cont, size, freq, ornt, phase = randomgenerator()
print(str(cont) + ", " + str(size) + ", " + str(freq) + ", " + str(ornt) + ", " + str(phase) + ", ") #print randomly generated parameters

#making file
dataPath='D:\\test\\'
date = (time.strftime("%Y-%m-%d"))
directory = dataPath+date
if not os.path.isdir(directory):
    print('path not exist')
    os.makedirs(directory)
logFilePath =dataPath+date+'\\'+Path(__file__).stem #filepath
i = 0
FileName = f"{i:03}"+'.txt'
while os.path.exists(logFilePath+FileName):
    i = i+1
    FileName = f"{i:03}"+'.txt'
print(logFilePath+FileName) #new file name and location

#logging
timestamp = (time.strftime("%M-%S"))
print(timestamp)
stimarray = numpy.array([cont, size, freq, ornt, phase])
print(stimarray)
fmt = "%1.3f"
numpy.savetxt(logFilePath+FileName,stimarray,fmt=fmt,delimiter = ',',newline = '\n')