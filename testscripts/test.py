from psychopy import visual, core, event #import some libraries from PsychoPy
from pathlib import Path

print(Path(__file__).name)

#create a window
mywin = visual.Window([1920,1080],monitor="Acer", units="deg",screen = 1)

frame_rate = mywin.getActualFrameRate(nIdentical=60, nMaxFrames=100,nWarmUpFrames=10, threshold=10)
print(frame_rate)

#create some stimuli
grating = visual.GratingStim(win=mywin, mask='circle', size=40, pos=[0,0], sf=0.2)
fixation = visual.GratingStim(win=mywin, size=0.2, pos=[0,0], sf=0, rgb=-1)

#draw the stimuli and update the window
while True: #this creates a never-ending loop
        
    grating.setPhase(0.05, '+')#advance phase by 0.05 of a cycle
    grating.draw()
    fixation.draw()
    mywin.flip()
    
    if event.getKeys(keyList = ['escape'], modifiers=False, timeStamped=False):
        break
    event.clearEvents()

#cleanup
mywin.close()
core.quit()