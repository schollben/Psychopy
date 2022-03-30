import sys
sys.path.append("C:/Users/fitzlab1/Desktop/psychopy/triggers") #path to trigger classes
import UniversalLibrary as UL
boardNum = 1
baseState = 0
gain =  UL.UNI4VOLTS
UL.cbAOut(boardNum,0,gain,0)
