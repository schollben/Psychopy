from psychopy import visual, logging, core
import pylab

# If you are having frame drops, try running this on a set of monitors that are
# *exactly* the same hardware. Mixing different monitor brands, even stuff with the same specs,
# caused frame drops in my testing. Once all the monitors were identical, frame drops went 
# down to 0.

mywin = visual.Window([1920,1080], fullscr=True,screen=1)
mywin.setRecordFrameIntervals(True)
mywin._refreshThreshold=1/120.0+0.004 #i've got 120Hz monitor and want to allow 4ms tolerance

#set the log module to report warnings to the std output window (default is errors only)
logging.console.setLevel(logging.WARNING)

#create some stimuli
stim1 = visual.PatchStim(win=mywin,tex='tri',mask='circle',units='pix',pos=(-200,-200),size=(500,500), sf=0.001, colorSpace='rgb', contrast=1.0)
stim2 = visual.PatchStim(win=mywin,tex='tri',mask='circle',units='pix',pos=(400,200),size=(500,500), sf=0.001, colorSpace='rgb', contrast=1.0)
stim1.setAutoDraw(False)
stim2.setAutoDraw(False)

clock = core.Clock()
while clock.getTime()<10:
        if clock.getTime()>5:
            stim1.setPhase(0.001, '-')
            stim2.setPhase(0.001, '-')
            stim1.draw()
            stim2.draw()
        else:
            stim1.setPhase(0.001, '+')
            stim2.setPhase(0.001, '+')
            stim1.draw()
            stim2.draw()
        mywin.flip()#flip the screen. This will block until the monitor is ready for the flip.

pylab.plot(mywin.frameIntervals)
pylab.show()

mywin.saveFrameIntervals(fileName=None, clear=True)
