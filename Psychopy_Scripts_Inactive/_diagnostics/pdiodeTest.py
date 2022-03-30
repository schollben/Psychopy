from psychopy import visual, logging, core
from psychopy import log, event
from os import path
import matplotlib, pylab, math, numpy
import shutil
matplotlib.use('WXAgg')

# If you are having frame drops, try running this on a set of monitors that are
# *exactly* the same hardware. Mixing different monitor brands, even stuff with the same specs,
# caused frame drops in my testing. Once all the monitors were identical, frame drops went 
# down to 0.
thisfile=path.dirname(path.realpath(__file__))+'\\'+path.basename(__file__)
dst= 'C:\\'
print thisfile
print dst
shutil.copy(thisfile,dst)

mywin = visual.Window([1920,1080], fullscr=True,screen=1)
mywin.setRecordFrameIntervals(True)
mywin._refreshThreshold=1/120.0+0.004 #i've got 120Hz monitor and want to allow 4ms tolerance

#set the log module to report warnings to the std output window (default is errors only)
logging.console.setLevel(logging.WARNING)

#create some stimuli
barTexture = numpy.ones([256,256,3]);
stim1 =visual.PatchStim(win=mywin,tex=barTexture,mask='none',units='pix',pos=[-920,500],size=(100,100))
stim1.setAutoDraw(True)

clock = core.Clock()
while clock.getTime()<100:
    stim1.setContrast(-1)
    #stim1.setPos([-920,500])
    mywin.flip()#flip the screen. This will block until the monitor is ready for the flip.

    stim1.setContrast(1)
    #stim1.setPos([-920,0])
    mywin.flip()#flip the screen. This will block until the monitor is ready for the flip.





#calculate some values
intervalsMS = pylab.array(mywin.frameIntervals[1:])*1000
m=pylab.mean(intervalsMS)
sd=pylab.std(intervalsMS)
distString= "Mean=%.1fms,    s.d.=%.1f,    99%%CI=%.1f-%.1f" %(m,sd,m-3*sd,m+3*sd)
nTotal=len(intervalsMS)
nDropped=sum(intervalsMS>(1.5*m))
droppedString = "Dropped/Frames = %i/%i = %.3f%%" %(nDropped,nTotal,nDropped/float(nTotal))

#plot the frameintervals
pylab.figure(figsize=[20,10])
pylab.subplot(1,2,1)
pylab.plot(intervalsMS, '-')
pylab.ylabel('t (ms)')
pylab.xlabel('frame N')
pylab.title(droppedString)
#
pylab.subplot(1,2,2)
pylab.hist(intervalsMS, 50, normed=0, histtype='stepfilled')
pylab.xlabel('t (ms)')
pylab.ylabel('n frames')
pylab.title(distString)
pylab.show()
