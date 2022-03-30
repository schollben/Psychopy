from __future__ import division

import numpy
from math import pi

from psychopy import visual, logging, core, filters, event, monitors
from psychopy.visual.radial import RadialStim


#Concentric ring stimulus for Ben's ferrets



class ConcentricStim(RadialStim):
    
    def __init__(self, *args, **kwargs):
        super(ConcentricStim, self).__init__(*args, **kwargs)

        res=128
        onePeriodX, onePeriodY = numpy.mgrid[0:2*pi:1j*res, 0:2*pi:1j*res]
        sinusoid = numpy.sin(onePeriodX-pi/2)*numpy.sin(1)
        intensity = numpy.where(sinusoid>0, 1, -1)

        self.tex = intensity
        

mon= monitors.Monitor('dualmonitors')

def demo_concentric():
    win = visual.Window(size=[3840,1080],monitor=mon,fullscr=True,screen=1, allowGUI=False, waitBlanking=False)
    cStim = ConcentricStim(win, size=[3840,3840], units="pix")
    cStim.setAutoDraw(True)

    phase = 0

    while not event.getKeys():
        
        phase += 0.01
        cStim.setRadialPhase(phase)
        win.flip()


if __name__ == "__main__":
    demo_concentric()
    