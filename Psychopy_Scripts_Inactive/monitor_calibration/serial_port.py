import serial, time, re, threading

class SerialPort(object):
    # This class talks to an Arduino and reads the raw data from it, adding timestamps.
    # This data is read by both the training program and the live plotting display. 
    # SerialPort accepts write commands from the training program to command the stimulus tablet.
    
    def __init__(self, serialPortName):
        #serial port setup
        self.serialPortName = int(serialPortName[3:])-1
        self.baudRate = 57600 #All devices in lab standardize on 57600. If device isn't responding, make sure you're not set to 9600.
        print "Opening serial port [" + serialPortName + "] at " + str(self.baudRate) 
        self.ser = serial.Serial(self.serialPortName, self.baudRate, timeout=5)
        self.updates = []
        self.threadLock = threading.Lock()
        
        self.startTimeMillis = time.time()*1000
        
        self.stopFlag = False
        self.SLEEP_TIME = 0.0001 #prevents polling thread from eating up all the CPU
        
    def getUpdates(self):
        #returns all of the raw text received since the last poll.
        updatesToReturn = self.updates
        with self.threadLock:
            self.updates = []
        return updatesToReturn
    
    def readSerial(self):
        b = ''
        while b == '' and not self.stopFlag:
            try:
                b = self.ser.readline()
            except:
                #Catch the extremely rare and useless exception:
                #serial.serialutil.SerialException: ReadFile failed (WindowsError(0, 'The operation completed successfully.'))
                #Reportedly this is a bug in the library. Ugh.
                b = ''
                continue
        return b
    
    def readData(self):
        while not self.stopFlag:
            time.sleep(self.SLEEP_TIME)
            data = self.readSerial()
            t = time.time() #all incoming messages get timestamped
            byteStr = str(data).rstrip()
            if byteStr != '' and byteStr != '\n': 
                with self.threadLock:
                    self.updates.append((byteStr, t))
    
    def close(self):
        self.stopFlag = True
        time.sleep(0.1)
        self.ser.close()
    
    def write(self, command):
        cmd = command.rstrip() + "\n" #ensure newline
        self.ser.write(cmd)
    
    def startReadThread(self):
        self.stopFlag = False
        thread = threading.Thread(target=self.readData)
        thread.daemon = True
        thread.start()