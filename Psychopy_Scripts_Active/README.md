# Psychopy
Psychopy visual stimulus

## Description
Python scripts mainly using PsychoPy. 
This repository can be used to generate visual stimulus for experiments on ferrets. We are using this program to investigate the microstructure of the brain and look at the effects of different disease states on the primary visual cortex. This is examined via a viral injection carrying DNA into different brain regions. 

## Getting Started

### Dependencies

### Installing
* Python, Psychopy

### Notes
* The whole repository should be downloaded to MyDocuments. 
* For logging the whole script, be sure to change the username when setting path in logScript function in logFunction.py according to the computer you are using. 
* All the logs will be saved under D:\\Psychopy but you can change the path by adjusting the logFileNameGenerator function in logFunction.py. 
* logFunction.py should be saved under same folder with the stimulus script that you are trying to run if you want to use a function from logFunction.py  to save the data and the whole script. 

### Executing program
* logFunction.py : Logs the run data of stimulus and the whole script at the moment of running the program. Currently set to organize log data in .txt format with each file under the folder of a date when the program was ran, keeping track of the trial number of different stimuli. 
* OrientationContrast.py
* OrientationRadomDraw.py: 
* OrientationRandomBeta.py: Generates grating stimulus with randomly selected orientation, contrast, size, spatial frequency, and phase. Can adjust range of each parameter and distribution factor using randomgenerator.py. 
* gridStimulus.py : Generates randomly placed black and white flickering grid stimulus. Can adjust size, number, flickering rate, duration time, and number of subgrid. 
* noiseStimulus.py : Generates random white and pink grid in an alternating order placed in a random location for each flickering time. Can adjust the color and size of the grid and its flickering rate. 

## Help

## Version History
* 0.1
    * Initial Release

## License

## Credits
