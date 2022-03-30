from psychopy import visual, logging, core, filters, event, monitors
import pylab, math, random, numpy, time, imp, sys
from os import path
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") 



a = [1,1,]
b = [2,2]
c = numpy.array((a,b))
print c







#import os
#file_name =  os.path.basename(sys.argv[0])
#print file_name



get date and time of experiment
import time, os
timeInitialized = (time.strftime("%H:%M:%S"))
date = (time.strftime("%Y-%m-%d"))
make directory
stimDir = 'C:/Users/fitzlab1/Documents/psychopystimdata/' + date+'/'
if not os.path.isdir(stimDir):
    os.mkdir(stimDir)
    print 'made stimcode folder'
find experiment filename exists
done=False
exptnum=0
while not done:
    exptnum=exptnum+1
    if exptnum<10:
        filename=stimDir+'Exp00'+str(exptnum)+'.txt'
    elif exptnum<100 and exptnum>9:
        filename=stimDir+'Exp0'+str(exptnum)
    else:
        filename=stimDir+'Exp'+str(exptnum)
    if not os.path.isfile(filename):
        done=True
        print done
        print filename
        print exptnum

