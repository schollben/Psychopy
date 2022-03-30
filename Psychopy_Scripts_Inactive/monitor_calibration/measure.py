"""
Runs automatic monitor calibration using ColorCal MkII.
"""

from psychopy import monitors, visual

import time
import re
import numpy as np
import random


from serial_port import SerialPort

class Photometer():
    
    def __init__(self, serialPortName):
        self.ser = SerialPort(serialPortName)
        self.ser.startReadThread()

    def readValue(self):
        """
        Write "MES" to the serial port, then await reply. Replies look like this:
        OK00, 15.97, 16.30,  5.07        
        >
        OK00 is junk. First number is red, second is green, third is blue.
        Function will return tuple (red, green, blue).
        """

        self.ser.write("MES\n")
        time.sleep(4)
        updates = self.ser.getUpdates()
        if updates == []:
            print "Error reading from photometer. Got " + str(updates)
            return None
        else:
            for u in updates:
                if "OK" in u[0]:
                    #parse colors and return
                    (junk, red, green, blue) = re.findall("(\d+\.?\d*)", u[0])
                    return (red, green, blue)
        return None
        

class ContrastStepper():

    def __init__(self, serialPortName="COM3", screenNumber=1):
        self.smallest = 0
        self.largest = 0
        self.gamma = 0
        self.photometer = Photometer(serialPortName)
        
        #make a PsychoPy window on the given screen
        self.mon = monitors.Monitor("Yep")
        self.win = visual.Window(monitor=self.mon, size=[1600,900], screen=screenNumber)
        self.grating = visual.GratingStim(self.win, tex="sqr", units="pix", sf=0.02, contrast=1.0, size=[1600,900])
        self.grating.setAutoDraw(True)
        
        #Show a grating stimulus of different contrasts
        self.contrasts = np.arange(1,-0.1,-0.25)
        
    def measure(self):
        """
        Steps through contrasts and reads photometer at each step. Displays average (luminance).
        """
        for c in self.contrasts:
            self.grating.setContrast(c)
            self.win.flip()
            (r,g,b) = self.photometer.readValue()
            avg = round((float(r) + float(g) + float(b)) / 3, 2)
            print "contrast " + str(round(c,2)) + ": \t" + str(avg) + " \trgb: " + str((r,g,b))
    
    def test(self):
        """
        Quickly flashes between contrasts at random. Good for perceptually confirming your settings.
        """
        for i in range(len(self.contrasts) * 30):
            self.grating.setContrast(random.choice(self.contrasts))
            self.win.flip()
            time.sleep(0.25)

if __name__ == "__main__":
    cs = ContrastStepper()
    cs.measure()
    cs.test()