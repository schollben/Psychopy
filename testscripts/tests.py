import numpy, random

numCells = 5
totalNumStim = 10
stimOrder = numpy.arange(0,totalNumStim)
stimOrder = numpy.repeat(stimOrder,numCells)
random.shuffle(stimOrder)
stimOrder = stimOrder.reshape(numCells,totalNumStim)

for ncell in range(0,numCells):
    for k in range(0,totalNumStim):
        stimNumber = stimOrder[ncell,k]
        print(stimNumber)
